import gradio as gr
import pandas as pd
import plotly.graph_objects as go

from utils import computeMetrics, loadBasicDF, getReport

def visualiseNumCalls():
    """
    Create a visualization dashboard of call metrics using Plotly.
    
    Returns:
        plotly.graph_objects.Figure: A figure containing multiple subplots with call analytics
    """
    # Load data and compute metrics
    df = loadBasicDF()
    metrics = computeMetrics(df)

    bar_color_1 = '#d62828'  # Custom color for the first bar (dodger blue)
    bar_color_2 = '#f77f00'  # Custom color for the second bar (lime green)


    NumCallsFig = go.Figure(data=[
        go.Bar(
            name='last week', 
            x=["Calls last week"], 
            y=[metrics[0]],
            text=[metrics[0]],
            textposition='inside',
            marker_color=bar_color_1,
            textfont=dict(color='white'),
            marker=dict(line=dict(width=0)),
        ),
        go.Bar(
            name='total', 
            x=["Total Calls"], 
            y=[metrics[1]],
            text=[metrics[1]],
            textposition='inside',
            marker_color=bar_color_2,
            textfont=dict(color='white'),
            marker=dict(line=dict(width=0)),
        )
    ])

    NumCallsFig.update_traces(texttemplate='%{text}', textfont_size=12)
    NumCallsFig.update_yaxes(showticklabels=False)
    NumCallsFig.update_layout(
        xaxis=dict(
            tickfont=dict(color='red'),
            showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=300,
    )

    NumCallsFig.update_traces(hoverinfo='none', hovertemplate=None)

    NumCallsFig.update_layout(
        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'lasso2d', 'toImage', 'Logo'],
        dragmode=False
    )


    return NumCallsFig
    
def visualiseUniqueCallers():
    # Load data and compute metrics
    df = loadBasicDF()
    metrics = computeMetrics(df)


    col1 = "#d62828"
    col2 = "#f77f00"
    col3 = "#fcbf49"
    col4 = "#eae2b7"
    col5 = "#9b2226"

    labels = list(dict(metrics[3]).keys())
    values = [metrics[3][key] for key in labels]

    colors = [col1, col2, col3, col4, col5]  # List of colors to use

    fig = go.Figure(data=[go.Pie(labels=labels, 
                                values=values, 
                                marker=dict(colors=colors),
                                textinfo='value',  # Display both label and value
                                textfont_size=12,
                                insidetextorientation='radial',
                                hole=0.4)])

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=300,
    )

    fig.update_layout(
        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'lasso2d', 'toImage', 'Logo'],
        dragmode=False
    )

    return fig
        
def getReportdetailed(reportname:str):

    # test if reportname is valid - load report
    report = getReport(reportname)

    if report == False:
        raise ValueError("provided reportname is not valid")

    # get Summary
    summary = report["analysis"]["summary"]
    summary = f"""### Summary

    {summary}
    """

    # get Conversation
    conversation = report["artifact"]["messagesOpenAIFormatted"]
    # get Audio URL
    audiourl = report["artifact"]["stereoRecordingUrl"]

    return summary, audiourl, conversation


with gr.Blocks() as app:

    gr.HTML("""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Centered Heading</title>
        <style>h1 {text-align: center;}</style>
    </head>
    <body><h1>PhoneBot 📞</h1></body>""")



    with gr.Row():

        with gr.Column():
            numcalls_plot = gr.Plot(visualiseNumCalls(), show_label=False, container=False)

        with gr.Column():
            uniquecallers_plot = gr.Plot(visualiseUniqueCallers(), show_label=False, container=False)

    with gr.Tab("Reports Overview"):
        callsdf = gr.Dataframe(loadBasicDF())

        reloadbtn = gr.Button("refresh")

        reloadbtn.click(loadBasicDF, outputs=callsdf)

    with gr.Tab("Detailed Report"):

        with gr.Row():
            with gr.Column(scale=7):
                searchreport = gr.Textbox(lines=1, placeholder="Report Name e.g.: 1726236604538", show_label=False, container=False)
            with gr.Column(scale=1):
                searchbtn = gr.Button("🔎 load")

        gr.Markdown("----------")


        ReportSummary = gr.Markdown()
        ReportChat = gr.Chatbot(type="messages")
        ReportAudio = gr.Audio(type="filepath", container=False, show_label=False)

        searchbtn.click(getReportdetailed, inputs=searchreport, outputs=[ReportSummary, ReportAudio, ReportChat])




        




app.launch(
    auth=("Visana","V1sana"),
    server_port=8080, 
    share=False)