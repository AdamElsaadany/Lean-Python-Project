Lean Six Sigma Process Improvement via Python Simulation

Project Overview
This project uses a discrete-event simulation built in Python with the SimPy library to model a coffee shop's customer flow. The goal is to apply the DMAIC (Define, Measure, Analyze, Improve, Control) methodology to identify bottlenecks and demonstrate the impact of process improvements in a quantifiable, data-driven way.

The Results
The simulation proved that the initial process ("As-Is") with one barista was unable to handle the customer arrival rate, resulting in an average wait time of over 35 minutes. By implementing a simple process change—adding a second barista—we achieved a **93% reduction in average customer wait time**.

How to Run This Project
1.  Clone the repository: `git clone https://github.com/AdamElsaadany/Lean-Python-Project.git`
2.  Navigate to the project directory.
3.  Create and activate a virtual environment.
4.  Install the required libraries: `pip install -r requirements.txt`
5.  Run the simulation: `python simulation.py`

Tools Used
- Python
- SimPy: For the discrete-event simulation.
- Matplotlib: For data visualization.
- Lean Six Sigma (DMAIC): As the guiding methodology for process improvement.
