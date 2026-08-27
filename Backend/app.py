from report_generator import generate_pdf
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path

from analyzer import analyze_cfd_file
from visualization import create_graphs
from ai_assistant import (
    generate_summary,
    answer_question
)


app = FastAPI()

latest_results = None
latest_summary = None


app.mount(
    "/graphs",
    StaticFiles(directory="../generated"),
    name="graphs"
)


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>CFD AI Assistant</title>

        <style>

            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 0;
            }

            .header {
                background: #12355b;
                color: white;
                padding: 25px;
                text-align: center;
            }

            .header h1 {
                margin: 0;
                font-size: 32px;
            }

            .header p {
                margin-top: 8px;
                font-size: 16px;
            }

            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }

            .card {
                background: white;
                padding: 30px;
                margin-bottom: 25px;
                border-radius: 12px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.08);
            }

            .card h2 {
                color: #12355b;
            }

            .upload-box {
                text-align: center;
                padding: 30px;
                border: 2px dashed #aaa;
                border-radius: 10px;
            }

            input[type="file"] {
                margin: 20px;
            }

            button {
                background: #12355b;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 7px;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background: #1d5d91;
            }

            .features {
                display: grid;
                grid-template-columns:
                    repeat(3, 1fr);
                gap: 15px;
                margin-top: 20px;
            }

            .feature {
                background: #eef4fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }

            .footer {
                text-align: center;
                padding: 25px;
                color: #666;
            }

        </style>

    </head>


    <body>


        <div class="header">

            <h1>
                CFD AI Assistant
            </h1>

            <p>
                AI-assisted analysis of Computational Fluid Dynamics data
            </p>

        </div>


        <div class="container">


            <div class="card">

                <h2>
                    Upload CFD Simulation Data
                </h2>

                <p>
                    Upload the CSV file exported from your
                    ANSYS Fluent simulation.
                </p>


                <div class="upload-box">

                    <form
                        action="/analyze"
                        method="post"
                        enctype="multipart/form-data"
                    >

                        <input
                            type="file"
                            name="file"
                            accept=".csv"
                            required
                        >

                        <br>

                        <button type="submit">
                            Analyze CFD
                        </button>

                    </form>

                </div>

            </div>


            <div class="card">

                <h2>
                    What this application does
                </h2>


                <div class="features">

                    <div class="feature">

                        <h3>
                            CFD Analysis
                        </h3>

                        <p>
                            Calculates velocity,
                            pressure and flow parameters.
                        </p>

                    </div>


                    <div class="feature">

                        <h3>
                            Visualization
                        </h3>

                        <p>
                            Generates velocity and
                            pressure graphs.
                        </p>

                    </div>


                    <div class="feature">

                        <h3>
                            AI Feedback
                        </h3>

                        <p>
                            Explains CFD results using
                            a local AI model.
                        </p>

                    </div>

                </div>

            </div>


        </div>


        <div class="footer">

            CFD AI Assistant |
            ANSYS Fluids Dynamics Internship

        </div>


    </body>

    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):

    # -------------------------
    # SAVE UPLOADED FILE
    # -------------------------

    upload_folder = Path("../data/uploads")

    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_folder / file.filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)


    # -------------------------
    # CFD ANALYSIS
    # -------------------------

    results = analyze_cfd_file(
        str(file_path)
    )

    summary = generate_summary(
        results
    )

    global latest_results, latest_summary

    latest_results = results
    latest_summary = summary


    # -------------------------
    # CREATE GRAPHS
    # -------------------------

    create_graphs(
        str(file_path)
    )


    # -------------------------
    # AI ANALYSIS
    # -------------------------

    summary = generate_summary(
        results
    )


    # -------------------------
    # RESULTS PAGE
    # -------------------------

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>CFD Analysis Results</title>

<style>

body {{

    margin: 0;

    font-family: Arial, sans-serif;

    background: #f4f7fb;

    color: #222;
}}


.header {{

    background: #12355b;

    color: white;

    padding: 25px;

    text-align: center;
}}


.container {{

    max-width: 1100px;

    margin: 30px auto;

    padding: 20px;
}}


.card {{

    background: white;

    padding: 25px;

    margin-bottom: 25px;

    border-radius: 12px;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.08);
}}


.metrics {{

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;
}}


.metric {{

    background: #eef4fa;

    padding: 20px;

    border-radius: 10px;

    text-align: center;
}}


.metric h3 {{

    margin-top: 0;

    color: #555;
}}


.metric p {{

    font-size: 25px;

    font-weight: bold;

    color: #12355b;
}}


.graph {{

    width: 100%;

    max-width: 800px;

    display: block;

    margin: auto;

    border-radius: 8px;
}}


.ai {{

    background: #f7f9fc;

    padding: 20px;

    border-radius: 10px;

    white-space: pre-wrap;

    line-height: 1.7;
}}


.back {{

    display: inline-block;

    padding: 12px 20px;

    background: #12355b;

    color: white;

    text-decoration: none;

    border-radius: 7px;
}}


@media(max-width:700px) {{

    .metrics {{

        grid-template-columns: 1fr;

    }}

}}


</style>

</head>


<body>


<div class="header">

    <h1>
        CFD AI Assistant
    </h1>

    <p>
        CFD Simulation Analysis Dashboard
    </p>

</div>


<div class="container">


<!-- ========================= -->
<!-- CFD RESULTS -->
<!-- ========================= -->


<div class="card">

<h2>📊 CFD Results</h2>

<div class="card">

    <h2>
        💬 Ask CFD Assistant
    </h2>

    <p>
        Ask a question about this simulation.
    </p>

    <form
        action="/ask"
        method="post"
    >

        <input
            type="text"
            name="question"
            placeholder="Why is pressure decreasing?"
            required
            style="
                width: 70%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 7px;
            "
        >


        <input
            type="hidden"
            name="maximum_velocity"
            value="{results["maximum_velocity"]}"
        >

        <input
            type="hidden"
            name="minimum_velocity"
            value="{results["minimum_velocity"]}"
        >

        <input
            type="hidden"
            name="average_velocity"
            value="{results["average_velocity"]}"
        >

        <input
            type="hidden"
            name="maximum_pressure"
            value="{results["maximum_pressure"]}"
        >

        <input
            type="hidden"
            name="minimum_pressure"
            value="{results["minimum_pressure"]}"
        >

        <input
            type="hidden"
            name="pressure_drop"
            value="{results["pressure_drop"]}"
        >

        <input
            type="hidden"
            name="flow_rate"
            value="{results["flow_rate"]}"
        >

        <input
            type="hidden"
            name="reynolds_number"
            value="{results["reynolds_number"]}"
        >

        <input
            type="hidden"
            name="flow_regime"
            value="{results["flow_regime"]}"
        >

        <button
            type="submit"
            style="
                padding: 12px 20px;
                margin-left: 5px;
                background: #12355b;
                color: white;
                border: none;
                border-radius: 7px;
                cursor: pointer;
            "
        >

            Ask

        </button>

    </form>

</div>


<div class="metrics">


<div class="metric">

<h3>
Average Velocity
</h3>

<p>
{results["average_velocity"]:.4f}
m/s
</p>

</div>


<div class="metric">

<h3>
Maximum Velocity
</h3>

<p>
{results["maximum_velocity"]:.4f}
m/s
</p>

</div>


<div class="metric">

<h3>
Pressure Drop
</h3>

<p>
{results["pressure_drop"]:.2f}
Pa
</p>

</div>


<div class="metric">

<h3>
Flow Rate
</h3>

<p>
{results["flow_rate"]:.6f}
m³/s
</p>

</div>


<div class="metric">

<h3>
Reynolds Number
</h3>

<p>
{results["reynolds_number"]:.0f}
</p>

</div>


<div class="metric">

<h3>
Flow Regime
</h3>

<p>
{results["flow_regime"]}
</p>

</div>


</div>

</div>


<!-- ========================= -->
<!-- VELOCITY -->
<!-- ========================= -->


<div class="card">

<h2>
📈 Velocity Distribution
</h2>

<p>
Velocity variation along the pipe.
</p>

<img
    class="graph"
    src="/graphs/velocity.png"
>

</div>


<!-- ========================= -->
<!-- PRESSURE -->
<!-- ========================= -->


<div class="card">

<h2>
📉 Pressure Distribution
</h2>

<p>
Pressure variation along the pipe.
</p>

<img
    class="graph"
    src="/graphs/pressure.png"
>

</div>


<!-- ========================= -->
<!-- AI -->
<!-- ========================= -->


<div class="card">

<h2>
🤖 AI CFD Analysis
</h2>

<div class="ai">

{summary}

</div>

</div>


<a
    class="back"
    href="/"
>
    ← Analyze Another Simulation
</a>


</div>


</body>

</html>
"""

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(
    question: str
):

    


    answer = answer_question(
         latest_results,
        question
    )


    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>CFD AI Answer</title>

        <style>

            body {{
                font-family: Arial;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                background: #f4f7fb;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 12px;
                margin-bottom: 20px;
                box-shadow:
                    0 3px 12px
                    rgba(0,0,0,0.08);
            }}

            .answer {{
                white-space: pre-wrap;
                line-height: 1.7;
            }}

            a {{
                text-decoration: none;
                color: #12355b;
            }}

        </style>

    </head>


    <body>

        <div class="card">

            <h2>
                Your Question
            </h2>

            <p>
                {question}
            </p>

        </div>


        <div class="card">

            <h2>
                🤖 CFD AI Assistant
            </h2>

            <div class="answer">

                {answer}

            </div>

        </div>


        <a href="/">
            ← Back to CFD Assistant
        </a>

    </body>

    </html>
    """
@app.get("/download_report")
async def download_report():

    if latest_results is None:
        return {"error": "Please analyze a file first"}

    output_path = "../generated/CFD_Report.pdf"

    generate_pdf(
        latest_results,
        latest_summary,
        output_path
    )

    if not os.path.exists(output_path):
        return {"error": "Report not generated"}

    return FileResponse(
        path=output_path,
        filename="CFD_Report.pdf",
        media_type="application/pdf"
    )