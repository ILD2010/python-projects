# 🛡️ Sentinel Lab
### Interactive Python SOC Simulator

Sentinel Lab is a **terminal-based Security Operations Center (SOC) simulator** built with Python. It generates fictional web traffic, detects suspicious activity, and allows users to investigate security alerts through an interactive dashboard.

I created this project to explore **SOC operations, detection engineering, Python development, and terminal-based user interface design**.

##  Features

- **Traffic Simulation** — Generate fictional normal and suspicious web requests.
- **Threat Detection** — Identify SQL injection, directory traversal, scanner activity, and other suspicious patterns.
- **Alert Dashboard** — View alert IDs, timestamps, source IPs, severity, threat scores, and investigation status.
- **Interactive Investigations** — Examine alerts, add notes, change severity, and dismiss findings.
- **Filtering** — Filter displayed alerts to focus on specific activity.
- **JSON Storage** — Save and manage alert information.
- **Modular Design** — Multiple Python modules working together as one application.

##  Installation & Usage

**Requirements:** Python 3.11+ recommended.

**1. Download the repository**

Click **Code → Download ZIP** on GitHub and extract the folder, or clone it:

```bash
git clone https://github.com/ILD2010/python-projects/blob/main/sentinel_lab
```

**2. Open the project**

Open the downloaded folder in VS Code or navigate to it using your terminal.

**3. Run Sentinel Lab**

From the directory containing `main.py`, execute:

```bash
python3 main.py
```

The interactive SOC dashboard will launch in your terminal.

No Docker container or virtual environment is required.

If your installation requires additional Python packages, install the dependencies listed in `requirements.txt`.

##  How It Works

Once launched, Sentinel Lab provides an interactive menu:

| Option | Function |
|---|---|
| Generate Traffic | Simulate new web traffic and detect threats |
| Investigate Alerts | Review alerts, add notes, and update their status |
| Filter View | Narrow the displayed alerts |
| Reset | Reset the simulation |
| Exit | Close the application |

Follow the on-screen prompts to interact with the simulator.

##  Project Structure

```text
Sentinel-Lab/
├── main.py                 # Application entry point
├── sentinel/
│   ├── models.py           # Data models
│   ├── generator.py        # Traffic simulation
│   ├── rules.py            # Detection rules
│   ├── analyzer.py         # Threat analysis and scoring
│   ├── store.py            # JSON storage
│   └── dashboard.py        # Interactive terminal UI
├── tests/                  # Unit tests
└── README.md
```

##  Testing

Run the automated tests with:

```bash
python3 -m unittest discover -s tests -v
```

##  Project Purpose

Sentinel Lab was built as a personal cybersecurity and Python development project to gain hands-on experience with:

- SOC alert monitoring and investigation
- Security detection rules and risk scoring
- Python object-oriented programming
- Multi-module application architecture
- Interactive terminal interfaces
- JSON data management and automated testing

##  Disclaimer

Sentinel Lab is an **educational, defensive security simulator**. All traffic and IP addresses are fictional and generated locally.

It does not scan real networks, send attack requests, or interact with external systems.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
