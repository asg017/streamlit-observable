import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "streamlit-component-lib"
import { Runtime, Inspector } from "@observablehq/runtime";
import debounceExecution from "./debounceExecution"

class Observable extends StreamlitComponentBase<{}> {
  public observeValue = {};
  private notebookRef = React.createRef<HTMLDivElement>();
  private runtime: any = null;
  private main: any = null;
  private debounceUpdate: any = null;

  componentWillUnmount() {
    this.runtime?.dispose();
  }
  // @ts-ignore
  public componentDidUpdate(prevProps: any) {
    const { args: prevArgs } = prevProps;
    if (prevArgs.notebook !== this.props.args.notebook) {
      // TODO handle new notebook
    }
    if (prevArgs.debounce !== this.props.args.debounce) {
      this.setupDebounceUpdate(this.props.args.debounce)
    }
    if (this.main) {
      this.redefineCells(this.main, this.props.args.redefine);
    }
  }

  async embedNotebook(notebook: string, targets: string[], observe: string[], hide: string[], debounce: number) {
    if (this.runtime) {
      this.runtime.dispose();
    }
    this.setupDebounceUpdate(debounce)
    const targetSet = new Set(targets);
    const observeSet = new Set(observe);
    const hideSet = new Set(hide);
    this.runtime = new Runtime();
    const { default: define } = await eval(`import("https://api.observablehq.com/${notebook}.js?v=3")`); // eslint-disable-line no-eval
    this.main = this.runtime.module(define, (name: string) => {
      if (observeSet.has(name) && !targetSet.has(name)) {
        const observeValue = this.observeValue;
        return {
          fulfilled: (value: any) => {
            //@ts-ignore
            observeValue[name] = value;
            this.debounceUpdate()
          }
        }
      }
      if (targetSet.size > 0 && !targetSet.has(name)) return;
      if(hideSet.has(name)) return true;
      const el = document.createElement('div');
      this.notebookRef.current?.appendChild(el);

      const i = new Inspector(el);

      const ResizeObserver = (window as any).ResizeObserver
      if (ResizeObserver) {
        const resizeObserver = new ResizeObserver(() => {
          Streamlit.setFrameHeight();
        })
        resizeObserver.observe(el)
      }
      el.addEventListener('input', () => {
        Streamlit.setFrameHeight();
      })
      return {
        pending() {
          i.pending();
          Streamlit.setFrameHeight();
        },
        fulfilled(value: any) {
          i.fulfilled(value);
          Streamlit.setFrameHeight();
        },
        rejected(error: any) {
          i.rejected(error);
          Streamlit.setFrameHeight();
        },
      };
    });
    if (observeSet.size > 0) {
      Promise.all(Array.from(observeSet).map(async name => [name, await this.main.value(name)])).then(initial => {
        for (const [name, value] of initial) {
          // @ts-ignore
          this.observeValue[name] = value
        }
        this.debounceUpdate()
      })
    }
  }

  private setupDebounceUpdate(debounce: any) {
    if (debounce) {
      this.debounceUpdate = debounceExecution(() => Streamlit.setComponentValue(this.observeValue), debounce)
    } else {
      this.debounceUpdate = () => Streamlit.setComponentValue(this.observeValue)
    }
  }

  redefineCells(main: any, redefine = {}) {
    for (let cell in redefine) {
      //@ts-ignore
      main.redefine(cell, redefine[cell]);
    }
  }
  componentDidMount() {
    const { notebook, targets = [], observe = [], redefine = {} , hide = [], debounce = 0 } = this.props.args;
    this.embedNotebook(notebook, targets, observe, hide, debounce).then(() => {
      this.redefineCells(this.main, redefine);
    });

  }

  public render = (): ReactNode => {
    return (
      <div style={{ border: '1px solid gray', borderRadius: '4px' }}>
        <div style={{ padding: '9px 12px' }}>
          <div ref={this.notebookRef}></div>
        </div>
        <div style={{ marginTop: '4px' }}>
          
          <div style={{
            backgroundColor: '#ddd',
            fontWeight: 700,
            padding: ".25rem .5rem",
            borderRadius: '0 0 4px 4px',
            gridTemplateColumns: "auto auto",
            display:"grid"
          }}>
            <div style={{textAlign:"left"}}>{this.props.args.name}</div>
            <div style={{textAlign:"right"}}>
            <a target="_blank" rel="noopener noreferrer" href={`https://observablehq.com/${this.props.args.notebook}`} style={{ color: '#666', }}>{this.props.args.notebook}</a>
            </div>
          </div>
        </div>
      </div >
    )
  }
}

export default withStreamlitConnection(Observable)
