import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
import pandas as pd

df = pd.read_csv('DadosDRE.csv', sep=';')
checkbox_renderer = JsCode("""
class CheckboxRenderer{

    init(params) {
        this.params = params;

        this.eGui = document.createElement('input');
        this.eGui.type = 'checkbox';
        this.eGui.checked = params.value;

        this.checkedHandler = this.checkedHandler.bind(this);
        this.eGui.addEventListener('click', this.checkedHandler);
    }

    checkedHandler(e) {
        let checked = e.target.checked;
        let colId = this.params.column.colId;
        this.params.node.setDataValue(colId, checked);
    }

    getGui(params) {
        return this.eGui;
    }

    destroy(params) {
    this.eGui.removeEventListener('click', this.checkedHandler);
    }
}//end class
""")

builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_column('validado',  editable=True, cellRenderer=checkbox_renderer)
builder.configure_auto_height(False)
go = builder.build()

AgGrid(
    df,
    width=300,
    height=300,
    gridOptions=go,
    allow_unsafe_jscode=True
)

