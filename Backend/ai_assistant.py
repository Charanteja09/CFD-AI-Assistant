from ollama import chat
def create_prompt(results):

    prompt = f"""
You are a CFD engineering assistant.

Analyze the following CFD simulation of water flowing through
a straight pipe.

SIMULATION RESULTS

Maximum velocity: {results["maximum_velocity"]} m/s
Minimum velocity: {results["minimum_velocity"]} m/s
Average velocity: {results["average_velocity"]} m/s

Maximum pressure: {results["maximum_pressure"]} Pa
Minimum pressure: {results["minimum_pressure"]} Pa
Pressure drop: {results["pressure_drop"]} Pa

Flow rate: {results["flow_rate"]} m³/s

Reynolds number: {results["reynolds_number"]}
Flow regime: {results["flow_regime"]}


Prepare the analysis using these sections:

1. SIMULATION SUMMARY
Briefly explain what the simulation indicates.

2. VELOCITY ANALYSIS
Explain the velocity results and what they indicate about the flow.

3. PRESSURE ANALYSIS
Explain the pressure distribution and pressure drop.

4. FLOW REGIME
Explain the Reynolds number and why the flow is classified as
laminar, transitional, or turbulent.

5. IMPORTANT OBSERVATIONS
List the important findings from the simulation.

6. ENGINEERING FEEDBACK
Suggest what could be investigated or improved in a future simulation.

Use only the provided numerical results.
Do not invent CFD values.
Keep the explanation simple enough for a student to understand.
"""

    return prompt

def generate_summary(results):

    prompt = create_prompt(results)

    response = chat(
        model="gemma4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content

def answer_question(results, question):

    prompt = f"""
You are a CFD engineering assistant.

The user is asking a question about a CFD simulation.

Use the following VERIFIED simulation results:

Maximum velocity:
{results["maximum_velocity"]} m/s

Minimum velocity:
{results["minimum_velocity"]} m/s

Average velocity:
{results["average_velocity"]} m/s

Maximum pressure:
{results["maximum_pressure"]} Pa

Minimum pressure:
{results["minimum_pressure"]} Pa

Pressure drop:
{results["pressure_drop"]} Pa

Flow rate:
{results["flow_rate"]} m³/s

Reynolds number:
{results["reynolds_number"]}

Flow regime:
{results["flow_regime"]}


USER QUESTION:

{question}


Instructions:

- Answer specifically about this simulation.
- Use the provided numerical results.
- Explain the answer simply.
- Do not invent measurements.
- If the question cannot be answered from the available
  data, clearly say that more CFD information is required.
"""

    response = chat(
        model="gemma4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content