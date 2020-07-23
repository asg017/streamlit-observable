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

  componentDidMount() {
    const { notebook, targets = [], redefine, observe = [] } = this.props.args;
    const targetSet = new Set(targets);
    const observeSet = new Set(observe);
    const runtime = new Runtime();
    const observeValue = this.observeValue;
    // @ ts-ignore
    eval(`import("https://api.observablehq.com/${notebook}.js?v=3")`).then((d: any) => {
      const define = d.default;
      console.log(define, this.notebookRef.current);
      const main = runtime.module(define, (name: string) => {
        if (observeSet.has(name) && !targetSet.has(name)) {
          return {
            fulfilled(value: any) {
              //@ts-ignore
              observeValue[name] = value;
              //@ts-ignore
              Streamlit.setComponentValue(observeValue);
            }
          }
        }
        if (targetSet.size > 0 && !targetSet.has(name)) return;

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
      for (let cell in redefine) {
        main.redefine(cell, redefine[cell]);
      }
      if (observeSet.size > 0) {
        Promise.all(Array.from(observeSet).map(async name => [name, await main.value(name)])).then(initial => {
          initial.map(([name, value]) => {
            // @ts-ignore
            this.observeValue[name] = value
          });
          Streamlit.setComponentValue(this.observeValue);
        })
      }
    })

  }

  public render = (): ReactNode => {
    return (
      <div>
        <div ref={this.notebookRef}></div>
      </div >
    )
  }
}

export default withStreamlitConnection(Observable)
