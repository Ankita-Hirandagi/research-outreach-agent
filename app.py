from flask import Flask, render_template, request, send_file
import pandas as pd
from agent_outreach import generate_outreach
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    table_data = []

    if request.method == "POST":
        file = request.files["file"]
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            data = {
                "researcher_name": row["researcher_name"],
                "institution": row["institution"],
                "article_title": row["article_title"],
                "article_summary": row["article_summary"],
                "signal_strength": row["signal_strength"],
                "contact_channel": row["contact_channel"]
            }

            message = generate_outreach(data)
            results.append(message)

            row_data = data.copy()
            row_data["generated_message"] = message
            table_data.append(row_data)

        # Save results in memory
        app.config["RESULT_DF"] = pd.DataFrame(table_data)

    return render_template("index.html", results=results)


@app.route("/download")
def download():
    df = app.config.get("RESULT_DF")

    if df is None:
        return "No data available"

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="outreach_results.csv"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)