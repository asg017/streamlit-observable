import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"
import { Runtime, Inspector } from "@observablehq/runtime";

class Observable extends StreamlitComponentBase<{}> {
  public observeValue = {};
  private notebookRef = React.createRef<HTMLDivElement>();
  private runtime: any = null;
  private main: any = null;

  componentWillUnmount() {
    this.runtime?.dispose();
  }
  // @ts-ignore
  public componentDidUpdate(prevProps: any) {
    const { args: prevArgs } = prevProps;
    if (prevArgs.notebook !== this.props.args.notebook) {
      // TODO handle new notebook
    }
    this.redefineCells(this.main, this.props.args.redefine);
  }

  async embedNotebook(notebook: string, targets: string[], observe: string[], hide:string[]) {
    if (this.runtime) {
      this.runtime.dispose();
    }
    const targetSet = new Set(targets);
    const observeSet = new Set(observe);
    const hideSet = new Set(hide);
    this.runtime = new Runtime();
    const { default: define } = await eval(`import("https://api.observablehq.com/${notebook}.js?v=3")`);
    this.main = this.runtime.module(define, (name: string) => {
      if (observeSet.has(name) && !targetSet.has(name)) {
        const observeValue = this.observeValue;
        return {
          fulfilled: (value: any) => {
            //@ts-ignore
            observeValue[name] = value;
            //@ts-ignore
            Streamlit.setComponentValue(observeValue);
          }
        }
      }
      if (targetSet.size > 0 && !targetSet.has(name)) return;
      if(hideSet.has(name)) return true;
      const el = document.createElement('div');
      this.notebookRef.current?.appendChild(el);

      const i = new Inspector(el);
      el.addEventListener('input', e => {
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
        };
        Streamlit.setComponentValue(this.observeValue);
      })
    }
  }

  redefineCells(main: any, redefine = {}) {
    for (let cell in redefine) {
      //@ts-ignore
      main.redefine(cell, redefine[cell]);
    }
  }
  componentDidMount() {
    const { notebook, targets = [], observe = [], redefine = {} , hide=[]} = this.props.args;
    Streamlit.setComponentValue(this.observeValue);
    this.embedNotebook(notebook, targets, observe, hide).then(() => {
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
            <a href={`https://observablehq.com/${this.props.args.notebook}`} style={{ color: '#666', }}>{this.props.args.notebook}</a>
            </div>
          </div>
        </div>
      </div >
    )
  }
}

export default withStreamlitConnection(Observable)
