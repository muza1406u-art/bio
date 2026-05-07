"""Streamlit app for an interactive computational biology cell atlas.

Run locally with:
    streamlit run app.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import plotly.graph_objects as go
import streamlit as st


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, ...]
    answer: str
    explanation: str


@dataclass(frozen=True)
class CellProfile:
    name: str
    kingdom: str
    summary: str
    theory: tuple[str, ...]
    labels: tuple[str, ...]
    quiz: tuple[QuizQuestion, ...]
    color: str
    shape: str


STUDENT_DETAILS = {
    "Name": "Ummarvali muzakir",
    "Registration number": "RA2511026050021",
    "Department": "CSE Aiml",
    "Section": "A",
}

CELL_PROFILES: tuple[CellProfile, ...] = (
    CellProfile(
        name="Animal Cell",
        kingdom="Eukaryotic",
        summary="A flexible membrane-bound eukaryotic cell that performs specialized functions in animals.",
        theory=(
            "Animal cells contain a nucleus, mitochondria, endoplasmic reticulum, Golgi body, lysosomes, ribosomes, and a plasma membrane.",
            "Computational biology models animal cells to understand gene expression, cancer growth, tissue engineering, and drug response.",
            "Unlike plant cells, animal cells do not have a rigid cell wall or chloroplasts, which allows many shapes and movement patterns.",
        ),
        labels=("Plasma membrane", "Nucleus", "Mitochondria", "Golgi body", "Rough ER", "Lysosome", "Ribosomes"),
        quiz=(
            QuizQuestion(
                "Which organelle is the main site of ATP production in animal cells?",
                ("Nucleus", "Mitochondria", "Golgi body", "Lysosome"),
                "Mitochondria",
                "Mitochondria perform aerobic respiration and produce most cellular ATP.",
            ),
            QuizQuestion(
                "Which structure controls movement of substances into and out of an animal cell?",
                ("Plasma membrane", "Cell wall", "Chloroplast", "Vacuole"),
                "Plasma membrane",
                "The selectively permeable plasma membrane regulates transport.",
            ),
        ),
        color="#7dd3fc",
        shape="sphere",
    ),
    CellProfile(
        name="Plant Cell",
        kingdom="Eukaryotic",
        summary="A photosynthetic eukaryotic cell with a cell wall, chloroplasts, and a large central vacuole.",
        theory=(
            "Plant cells convert light energy into chemical energy using chloroplasts and support the plant body with cellulose-rich cell walls.",
            "The large central vacuole stores water and solutes, maintains turgor pressure, and contributes to plant rigidity.",
            "Computational models of plant cells help predict photosynthesis, crop yield, stress responses, and gene regulation.",
        ),
        labels=("Cell wall", "Plasma membrane", "Nucleus", "Chloroplast", "Central vacuole", "Mitochondria", "Golgi body"),
        quiz=(
            QuizQuestion(
                "Which plant cell organelle carries out photosynthesis?",
                ("Mitochondrion", "Chloroplast", "Nucleus", "Ribosome"),
                "Chloroplast",
                "Chloroplasts contain chlorophyll and convert light energy into sugars.",
            ),
            QuizQuestion(
                "What is a major function of the central vacuole?",
                ("Protein synthesis", "Turgor pressure", "DNA replication", "Flagellar motion"),
                "Turgor pressure",
                "The central vacuole stores water and helps keep plant tissues firm.",
            ),
        ),
        color="#86efac",
        shape="box",
    ),
    CellProfile(
        name="Bacterial Cell",
        kingdom="Prokaryotic",
        summary="A small prokaryotic cell without a membrane-bound nucleus, often protected by a cell wall.",
        theory=(
            "Bacterial cells contain a nucleoid region, plasmids, ribosomes, cytoplasm, a plasma membrane, and usually a peptidoglycan cell wall.",
            "Some bacteria have capsules, pili, or flagella that help with protection, attachment, and movement.",
            "Computational biology is used to analyze bacterial genomes, antibiotic resistance, microbiomes, and infection spread.",
        ),
        labels=("Capsule", "Cell wall", "Plasma membrane", "Nucleoid DNA", "Plasmid", "Ribosomes", "Flagellum"),
        quiz=(
            QuizQuestion(
                "Where is bacterial genetic material mainly found?",
                ("Nucleoid", "Nucleus", "Chloroplast", "Vacuole"),
                "Nucleoid",
                "Bacteria do not have a membrane-bound nucleus; DNA is concentrated in the nucleoid.",
            ),
            QuizQuestion(
                "Which structure commonly helps bacteria move?",
                ("Flagellum", "Chloroplast", "Golgi body", "Central vacuole"),
                "Flagellum",
                "A flagellum rotates or waves to propel many bacterial cells.",
            ),
        ),
        color="#fbbf24",
        shape="rod",
    ),
    CellProfile(
        name="Fungal Cell",
        kingdom="Eukaryotic",
        summary="A eukaryotic cell with a chitin-rich cell wall; examples include yeast and mold cells.",
        theory=(
            "Fungal cells have nuclei, mitochondria, vacuoles, ribosomes, membranes, and cell walls made mainly of chitin and glucans.",
            "Yeast cells are single-celled fungi, while many fungi grow as thread-like hyphae that form mycelium.",
            "Computational biology supports fungal genome annotation, antifungal drug discovery, fermentation design, and ecosystem studies.",
        ),
        labels=("Chitin cell wall", "Plasma membrane", "Nucleus", "Vacuole", "Mitochondria", "ER", "Ribosomes"),
        quiz=(
            QuizQuestion(
                "What major polymer strengthens fungal cell walls?",
                ("Cellulose", "Chitin", "Peptidoglycan", "Keratin"),
                "Chitin",
                "Fungal cell walls are rich in chitin, unlike plant walls that are rich in cellulose.",
            ),
            QuizQuestion(
                "Fungal cells are classified as which cell type?",
                ("Prokaryotic", "Eukaryotic", "Acellular", "Viral"),
                "Eukaryotic",
                "Fungal cells contain membrane-bound nuclei and organelles.",
            ),
        ),
        color="#c084fc",
        shape="sphere",
    ),
    CellProfile(
        name="Protist Cell",
        kingdom="Eukaryotic",
        summary="A diverse eukaryotic cell type found in algae, amoebae, and protozoans.",
        theory=(
            "Protists may be photosynthetic, heterotrophic, or mixotrophic, and many live in aquatic or moist environments.",
            "Common structures include nucleus, mitochondria, contractile vacuoles, cilia, flagella, pseudopodia, and sometimes chloroplasts.",
            "Computational biology helps compare protist genomes, trace evolution, monitor harmful algal blooms, and study parasites.",
        ),
        labels=("Cell membrane", "Nucleus", "Contractile vacuole", "Mitochondria", "Cilia/flagellum", "Food vacuole", "Cytoplasm"),
        quiz=(
            QuizQuestion(
                "Which structure helps many freshwater protists remove excess water?",
                ("Contractile vacuole", "Cell wall", "Nucleoid", "Capsule"),
                "Contractile vacuole",
                "Contractile vacuoles pump out excess water to maintain osmotic balance.",
            ),
            QuizQuestion(
                "Protists are best described as what?",
                ("Only bacteria", "Diverse eukaryotes", "Only viruses", "Only animal tissues"),
                "Diverse eukaryotes",
                "Protists include many unrelated eukaryotic lineages.",
            ),
        ),
        color="#fb7185",
        shape="sphere",
    ),
    CellProfile(
        name="Neuron",
        kingdom="Specialized animal cell",
        summary="A nerve cell specialized for electrical and chemical communication.",
        theory=(
            "Neurons contain a cell body, nucleus, dendrites, axon, synaptic terminals, mitochondria, and sometimes myelin insulation.",
            "They receive signals through dendrites, process information in the cell body, and transmit impulses along the axon.",
            "Computational neuroscience uses mathematical models to simulate neuron firing, neural circuits, learning, and brain disorders.",
        ),
        labels=("Dendrites", "Cell body", "Nucleus", "Axon", "Myelin sheath", "Synaptic terminals", "Mitochondria"),
        quiz=(
            QuizQuestion(
                "Which neuron part usually carries signals away from the cell body?",
                ("Axon", "Dendrite", "Nucleus", "Ribosome"),
                "Axon",
                "The axon transmits action potentials away from the soma toward terminals.",
            ),
            QuizQuestion(
                "What is a key role of myelin?",
                ("Slow signaling", "Speed signal conduction", "Digest proteins", "Store DNA"),
                "Speed signal conduction",
                "Myelin electrically insulates axons and increases conduction speed.",
            ),
        ),
        color="#60a5fa",
        shape="neuron",
    ),
    CellProfile(
        name="Red Blood Cell",
        kingdom="Specialized animal cell",
        summary="A biconcave blood cell specialized for transporting oxygen with hemoglobin.",
        theory=(
            "Mature human red blood cells lack a nucleus and most organelles, creating more space for hemoglobin.",
            "Their biconcave shape increases surface area for gas exchange and helps them squeeze through capillaries.",
            "Computational models can study oxygen transport, blood flow, anemia, malaria, and cell deformability.",
        ),
        labels=("Biconcave membrane", "Hemoglobin-rich cytoplasm", "Flexible cytoskeleton", "No nucleus", "Oxygen binding area"),
        quiz=(
            QuizQuestion(
                "What molecule allows red blood cells to carry oxygen?",
                ("Hemoglobin", "Chlorophyll", "Collagen", "Insulin"),
                "Hemoglobin",
                "Hemoglobin binds oxygen in the lungs and releases it in tissues.",
            ),
            QuizQuestion(
                "Mature human red blood cells usually lack which structure?",
                ("Nucleus", "Membrane", "Cytoplasm", "Hemoglobin"),
                "Nucleus",
                "Human RBCs eject the nucleus during maturation.",
            ),
        ),
        color="#ef4444",
        shape="disc",
    ),
    CellProfile(
        name="White Blood Cell",
        kingdom="Specialized animal cell",
        summary="An immune cell that identifies, attacks, or coordinates defenses against pathogens.",
        theory=(
            "White blood cells include lymphocytes, neutrophils, monocytes, eosinophils, and basophils, each with distinct immune roles.",
            "They can engulf pathogens, produce antibodies, release signaling molecules, and remember previous infections.",
            "Computational immunology predicts immune-cell behavior, vaccine response, inflammation, and immunotherapy outcomes.",
        ),
        labels=("Cell membrane", "Lobed nucleus", "Granules", "Cytoplasm", "Receptors", "Lysosomes", "Mitochondria"),
        quiz=(
            QuizQuestion(
                "Which body system uses white blood cells as key defenders?",
                ("Immune system", "Skeletal system", "Digestive system", "Integumentary system"),
                "Immune system",
                "White blood cells are central components of immune defense.",
            ),
            QuizQuestion(
                "Which white blood cell type can produce antibodies after activation?",
                ("B lymphocyte", "Red blood cell", "Platelet", "Neuron"),
                "B lymphocyte",
                "Activated B cells can become plasma cells that secrete antibodies.",
            ),
        ),
        color="#f8fafc",
        shape="sphere",
    ),
)


def ellipsoid_grid(
    center: tuple[float, float, float],
    radii: tuple[float, float, float],
    rows: int = 28,
    cols: int = 28,
) -> tuple[list[list[float]], list[list[float]], list[list[float]]]:
    """Create a smooth parametric ellipsoid grid for realistic 3D organelles."""
    x_grid: list[list[float]] = []
    y_grid: list[list[float]] = []
    z_grid: list[list[float]] = []
    for row in range(rows):
        theta = math.pi * row / (rows - 1)
        x_line: list[float] = []
        y_line: list[float] = []
        z_line: list[float] = []
        for col in range(cols):
            phi = 2 * math.pi * col / (cols - 1)
            x_line.append(center[0] + radii[0] * math.sin(theta) * math.cos(phi))
            y_line.append(center[1] + radii[1] * math.sin(theta) * math.sin(phi))
            z_line.append(center[2] + radii[2] * math.cos(theta))
        x_grid.append(x_line)
        y_grid.append(y_line)
        z_grid.append(z_line)
    return x_grid, y_grid, z_grid


def add_ellipsoid(
    fig: go.Figure,
    name: str,
    center: tuple[float, float, float],
    radii: tuple[float, float, float],
    color: str,
    opacity: float = 0.55,
) -> None:
    """Add a shaded 3D ellipsoid that represents a cell body or organelle."""
    x_grid, y_grid, z_grid = ellipsoid_grid(center, radii)
    fig.add_trace(
        go.Surface(
            x=x_grid,
            y=y_grid,
            z=z_grid,
            name=name,
            opacity=opacity,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            hovertemplate=f"{name}<extra></extra>",
        )
    )


def add_box(
    fig: go.Figure,
    name: str,
    color: str,
    x_radius: float,
    y_radius: float,
    z_radius: float,
    opacity: float,
) -> None:
    """Add a transparent cuboid for a plant/fungal cell wall."""
    fig.add_trace(
        go.Mesh3d(
            x=[-x_radius, x_radius, x_radius, -x_radius, -x_radius, x_radius, x_radius, -x_radius],
            y=[-y_radius, -y_radius, y_radius, y_radius, -y_radius, -y_radius, y_radius, y_radius],
            z=[-z_radius, -z_radius, -z_radius, -z_radius, z_radius, z_radius, z_radius, z_radius],
            i=[0, 0, 0, 1, 4, 4, 2, 3, 0, 1, 5, 6],
            j=[1, 2, 3, 5, 5, 6, 6, 7, 4, 5, 6, 7],
            k=[2, 3, 7, 6, 6, 7, 7, 4, 5, 6, 7, 4],
            color=color,
            opacity=opacity,
            name=name,
            hoverinfo="name",
        )
    )


def add_line(
    fig: go.Figure,
    name: str,
    points: tuple[tuple[float, float, float], ...],
    color: str,
    width: int = 6,
) -> None:
    fig.add_trace(
        go.Scatter3d(
            x=[point[0] for point in points],
            y=[point[1] for point in points],
            z=[point[2] for point in points],
            mode="lines",
            line={"color": color, "width": width},
            name=name,
            hovertemplate=f"{name}<extra></extra>",
        )
    )


def add_label(
    fig: go.Figure,
    label: str,
    anchor: tuple[float, float, float],
    text_position: tuple[float, float, float],
    color: str = "#0f172a",
) -> None:
    """Add a readable label with a leader line pointing to the exact structure."""
    add_line(fig, f"{label} pointer", (anchor, text_position), "#64748b", 2)
    fig.add_trace(
        go.Scatter3d(
            x=[text_position[0]],
            y=[text_position[1]],
            z=[text_position[2]],
            mode="markers+text",
            marker={"size": 4, "color": color},
            text=[label],
            textposition="middle center",
            name=label,
            hovertemplate=f"{label}<extra></extra>",
        )
    )


def add_mitochondrion(fig: go.Figure, center: tuple[float, float, float], label_position: tuple[float, float, float]) -> None:
    add_ellipsoid(fig, "Mitochondrion outer membrane", center, (0.28, 0.12, 0.14), "#fb7185", 0.82)
    add_line(
        fig,
        "Mitochondrial cristae",
        tuple((center[0] - 0.18 + step * 0.09, center[1], center[2] + 0.05 * math.sin(step)) for step in range(5)),
        "#7f1d1d",
        3,
    )
    add_label(fig, "Mitochondrion", center, label_position)


def add_golgi(fig: go.Figure, center: tuple[float, float, float], label_position: tuple[float, float, float]) -> None:
    for layer in range(4):
        offset = (layer - 1.5) * 0.06
        add_line(
            fig,
            "Golgi flattened sacs",
            (
                (center[0] - 0.24, center[1] + offset, center[2] - 0.05),
                (center[0], center[1] + offset + 0.04, center[2] + 0.02),
                (center[0] + 0.24, center[1] + offset, center[2] + 0.05),
            ),
            "#a855f7",
            5,
        )
    add_label(fig, "Golgi body", center, label_position)


def add_ribosomes(fig: go.Figure, centers: tuple[tuple[float, float, float], ...]) -> None:
    for center in centers:
        add_ellipsoid(fig, "Ribosome", center, (0.035, 0.035, 0.035), "#111827", 0.95)
    add_label(fig, "Ribosomes", centers[0], (-1.35, -0.95, 0.75))


def add_chloroplast(fig: go.Figure, center: tuple[float, float, float], label_position: tuple[float, float, float]) -> None:
    add_ellipsoid(fig, "Chloroplast", center, (0.28, 0.16, 0.11), "#22c55e", 0.85)
    for offset in (-0.08, 0.0, 0.08):
        add_line(
            fig,
            "Thylakoid stacks",
            ((center[0] - 0.16, center[1] + offset, center[2]), (center[0] + 0.16, center[1] + offset, center[2])),
            "#166534",
            4,
        )
    add_label(fig, "Chloroplast", center, label_position)


def add_eukaryote_common(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Nucleus", (0.0, 0.0, 0.08), (0.34, 0.29, 0.27), "#818cf8", 0.88)
    add_ellipsoid(fig, "Nucleolus", (0.09, -0.05, 0.14), (0.09, 0.08, 0.07), "#4338ca", 0.92)
    add_label(fig, "Nucleus", (0.0, 0.0, 0.35), (0.0, 1.38, 0.92))
    add_mitochondrion(fig, (-0.55, 0.35, -0.12), (-1.36, 0.8, -0.45))
    add_golgi(fig, (0.58, -0.34, 0.03), (1.38, -0.8, 0.45))
    add_ribosomes(fig, ((-0.36, -0.58, 0.2), (-0.18, -0.62, -0.05), (0.38, 0.52, -0.18), (0.62, 0.12, 0.28)))


def render_animal_cell(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Flexible plasma membrane", (0, 0, 0), (1.12, 0.9, 0.72), "#7dd3fc", 0.35)
    add_eukaryote_common(fig)
    add_ellipsoid(fig, "Lysosome", (0.22, 0.62, -0.24), (0.13, 0.12, 0.12), "#f97316", 0.86)
    add_line(fig, "Rough endoplasmic reticulum", ((-0.42, -0.12, 0.05), (-0.7, -0.24, 0.0), (-0.62, -0.42, 0.12)), "#38bdf8", 5)
    add_label(fig, "Plasma membrane", (1.08, 0, 0.08), (1.55, 0.15, 0.62))
    add_label(fig, "Rough ER", (-0.65, -0.28, 0.06), (-1.42, -0.38, 0.35))
    add_label(fig, "Lysosome", (0.22, 0.62, -0.24), (0.86, 1.06, -0.55))


def render_plant_cell(fig: go.Figure) -> None:
    add_box(fig, "Rigid cellulose cell wall", "#65a30d", 1.35, 0.98, 0.78, 0.18)
    add_box(fig, "Plasma membrane just inside wall", "#86efac", 1.22, 0.86, 0.66, 0.18)
    add_ellipsoid(fig, "Large central vacuole", (-0.22, 0.04, -0.03), (0.62, 0.5, 0.4), "#bae6fd", 0.5)
    add_ellipsoid(fig, "Nucleus", (0.54, -0.35, 0.16), (0.24, 0.22, 0.2), "#818cf8", 0.9)
    add_chloroplast(fig, (-0.74, 0.42, 0.18), (-1.55, 0.7, 0.62))
    add_chloroplast(fig, (0.5, 0.42, -0.28), (1.44, 0.78, -0.62))
    add_mitochondrion(fig, (0.7, -0.05, -0.2), (1.48, -0.2, -0.62))
    add_golgi(fig, (0.34, -0.62, -0.04), (1.22, -1.08, 0.25))
    add_label(fig, "Cell wall", (1.35, 0.3, 0.28), (1.7, 0.64, 0.8))
    add_label(fig, "Central vacuole", (-0.28, 0.05, 0.36), (-1.3, -0.28, 0.66))
    add_label(fig, "Nucleus", (0.54, -0.35, 0.36), (0.86, -1.12, 0.68))


def render_bacterial_cell(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Capsule", (0, 0, 0), (1.45, 0.48, 0.48), "#fde68a", 0.24)
    add_ellipsoid(fig, "Peptidoglycan cell wall", (0, 0, 0), (1.28, 0.4, 0.4), "#fbbf24", 0.42)
    add_ellipsoid(fig, "Plasma membrane", (0, 0, 0), (1.12, 0.32, 0.32), "#fef3c7", 0.38)
    add_line(fig, "Nucleoid DNA coil", tuple((-0.55 + 0.12 * step, 0.12 * math.sin(step), 0.08 * math.cos(step)) for step in range(10)), "#2563eb", 5)
    for center in ((0.44, -0.14, 0.05), (0.62, 0.08, -0.08)):
        add_line(fig, "Circular plasmid", tuple((center[0] + 0.08 * math.cos(t), center[1] + 0.08 * math.sin(t), center[2]) for t in [i * math.pi / 8 for i in range(17)]), "#7c3aed", 4)
    add_line(fig, "Flagellum", ((1.2, 0, 0), (1.65, 0.12, 0.12), (2.05, -0.1, -0.08), (2.48, 0.14, 0.06)), "#374151", 8)
    for x_pos in (-0.9, -0.45, 0.05, 0.5):
        add_line(fig, "Pilus", ((x_pos, 0.32, 0.1), (x_pos - 0.15, 0.66, 0.22)), "#92400e", 3)
    add_ribosomes(fig, ((-0.35, -0.18, 0.16), (0.0, 0.2, -0.14), (0.75, -0.08, 0.1)))
    add_label(fig, "Capsule", (-1.18, 0.24, 0.18), (-1.62, 0.66, 0.55))
    add_label(fig, "Nucleoid DNA", (-0.08, 0, 0.08), (-0.28, -0.86, 0.52))
    add_label(fig, "Plasmid", (0.62, 0.08, -0.08), (1.2, -0.62, -0.32))
    add_label(fig, "Flagellum", (1.95, -0.04, 0.0), (2.54, -0.44, 0.38))


def render_fungal_cell(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Chitin cell wall", (0, 0, 0), (1.08, 0.9, 0.76), "#c084fc", 0.32)
    add_ellipsoid(fig, "Plasma membrane", (0, 0, 0), (0.96, 0.78, 0.62), "#e9d5ff", 0.28)
    add_eukaryote_common(fig)
    add_ellipsoid(fig, "Storage vacuole", (-0.46, 0.0, -0.24), (0.24, 0.2, 0.18), "#bae6fd", 0.65)
    add_label(fig, "Chitin cell wall", (0.95, 0.18, 0.18), (1.48, 0.52, 0.66))
    add_label(fig, "Vacuole", (-0.46, 0.0, -0.08), (-1.18, 0.2, -0.62))


def render_protist_cell(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Irregular protist membrane", (0, 0, 0), (1.14, 0.82, 0.66), "#fb7185", 0.34)
    add_eukaryote_common(fig)
    add_ellipsoid(fig, "Contractile vacuole", (-0.62, 0.34, 0.24), (0.18, 0.18, 0.16), "#67e8f9", 0.8)
    add_ellipsoid(fig, "Food vacuole", (0.38, 0.54, -0.2), (0.16, 0.13, 0.13), "#f59e0b", 0.82)
    for angle in [i * math.pi / 5 for i in range(10)]:
        add_line(fig, "Cilia", ((1.02 * math.cos(angle), 0.75 * math.sin(angle), 0.0), (1.28 * math.cos(angle), 0.98 * math.sin(angle), 0.1 * math.sin(angle))), "#be123c", 3)
    add_label(fig, "Contractile vacuole", (-0.62, 0.34, 0.24), (-1.48, 0.72, 0.72))
    add_label(fig, "Cilia / flagella", (1.18, 0.0, 0.0), (1.7, -0.38, 0.46))
    add_label(fig, "Food vacuole", (0.38, 0.54, -0.2), (0.9, 1.12, -0.56))


def render_neuron(fig: go.Figure) -> None:
    add_ellipsoid(fig, "Neuron cell body / soma", (0, 0, 0), (0.58, 0.48, 0.42), "#60a5fa", 0.58)
    add_ellipsoid(fig, "Nucleus", (0.02, 0.0, 0.04), (0.2, 0.18, 0.16), "#818cf8", 0.9)
    for angle in (math.pi / 2, 5 * math.pi / 6, 7 * math.pi / 6, 3 * math.pi / 2):
        start = (0.35 * math.cos(angle), 0.35 * math.sin(angle), 0)
        mid = (0.9 * math.cos(angle), 0.82 * math.sin(angle), 0.18 * math.sin(angle))
        end = (1.35 * math.cos(angle), 1.22 * math.sin(angle), 0.28 * math.sin(angle))
        add_line(fig, "Branching dendrite", (start, mid, end), "#2563eb", 10)
        add_line(fig, "Dendrite branch", (mid, (mid[0] + 0.26 * math.cos(angle + 0.5), mid[1] + 0.26 * math.sin(angle + 0.5), mid[2] + 0.12)), "#2563eb", 5)
    add_line(fig, "Axon", ((0.52, 0, 0), (1.25, 0.04, 0.02), (2.05, -0.04, -0.02), (2.9, 0.02, 0.03)), "#1d4ed8", 12)
    for center_x in (1.05, 1.55, 2.05, 2.55):
        add_ellipsoid(fig, "Myelin sheath segment", (center_x, 0, 0.02), (0.18, 0.14, 0.14), "#fde68a", 0.85)
    add_line(fig, "Synaptic terminals", ((2.9, 0.02, 0.03), (3.22, 0.22, 0.12)), "#1d4ed8", 6)
    add_line(fig, "Synaptic terminals", ((2.9, 0.02, 0.03), (3.2, -0.2, -0.1)), "#1d4ed8", 6)
    add_label(fig, "Dendrites", (-0.8, 0.82, 0.2), (-1.5, 1.25, 0.58))
    add_label(fig, "Cell body", (0, 0, 0.42), (-0.25, -0.95, 0.75))
    add_label(fig, "Nucleus", (0.02, 0, 0.2), (0.55, -0.78, 0.5))
    add_label(fig, "Axon", (1.65, 0, 0), (1.78, -0.58, 0.42))
    add_label(fig, "Myelin sheath", (2.05, 0, 0.14), (2.35, 0.62, 0.48))
    add_label(fig, "Synaptic terminals", (3.12, 0.12, 0.08), (3.45, 0.62, 0.4))


def render_red_blood_cell(fig: go.Figure) -> None:
    radius_steps = 34
    angle_steps = 50
    x_grid: list[list[float]] = []
    y_grid: list[list[float]] = []
    z_grid: list[list[float]] = []
    for row in range(radius_steps):
        radius = row / (radius_steps - 1)
        x_line: list[float] = []
        y_line: list[float] = []
        z_line: list[float] = []
        for col in range(angle_steps):
            angle = 2 * math.pi * col / (angle_steps - 1)
            x_line.append(1.18 * radius * math.cos(angle))
            y_line.append(1.18 * radius * math.sin(angle))
            z_line.append(0.2 - 0.36 * math.exp(-(radius * 2.25) ** 2))
        x_grid.append(x_line)
        y_grid.append(y_line)
        z_grid.append(z_line)
    fig.add_trace(go.Surface(x=x_grid, y=y_grid, z=z_grid, colorscale=[[0, "#ef4444"], [1, "#ef4444"]], opacity=0.88, showscale=False, name="Biconcave membrane"))
    fig.add_trace(go.Surface(x=x_grid, y=y_grid, z=[[-z for z in line] for line in z_grid], colorscale=[[0, "#dc2626"], [1, "#dc2626"]], opacity=0.88, showscale=False, name="Lower biconcave membrane"))
    for center in ((-0.35, 0.15, 0.02), (0.0, -0.2, -0.02), (0.35, 0.18, 0.0)):
        add_ellipsoid(fig, "Hemoglobin-rich cytoplasm", center, (0.06, 0.06, 0.035), "#7f1d1d", 0.9)
    add_label(fig, "Biconcave membrane", (0.82, 0.58, 0.08), (1.45, 0.92, 0.48))
    add_label(fig, "Hemoglobin", (0.0, -0.2, -0.02), (-0.35, -1.24, 0.38))
    add_label(fig, "No nucleus", (0, 0, 0), (0.1, 0.0, 0.76))
    add_label(fig, "Flexible cytoskeleton", (-0.75, 0.45, -0.06), (-1.45, 0.68, -0.42))


def render_white_blood_cell(fig: go.Figure) -> None:
    add_ellipsoid(fig, "White blood cell membrane", (0, 0, 0), (1.05, 0.9, 0.76), "#f8fafc", 0.42)
    for center in ((-0.22, 0.1, 0.08), (0.1, -0.04, 0.02), (0.36, 0.14, -0.02)):
        add_ellipsoid(fig, "Lobed nucleus", center, (0.26, 0.2, 0.18), "#7c3aed", 0.86)
    granules = ((-0.64, 0.42, 0.18), (-0.52, -0.24, -0.18), (0.48, 0.46, 0.22), (0.62, -0.35, 0.02), (0.12, 0.62, -0.2))
    for center in granules:
        add_ellipsoid(fig, "Immune granule / lysosome", center, (0.07, 0.07, 0.06), "#f97316", 0.9)
    add_mitochondrion(fig, (-0.42, -0.48, 0.16), (-1.35, -0.88, 0.52))
    add_label(fig, "Cell membrane", (0.9, 0.1, 0.16), (1.48, 0.42, 0.62))
    add_label(fig, "Lobed nucleus", (0.1, -0.04, 0.2), (0.3, -1.12, 0.62))
    add_label(fig, "Granules", (0.48, 0.46, 0.22), (1.18, 1.0, 0.48))
    add_label(fig, "Surface receptors", (-0.92, 0.12, 0.18), (-1.48, 0.38, 0.72))


def build_cell_figure(profile: CellProfile) -> go.Figure:
    """Build a profile-specific labelled 3D diagram instead of a generic marker model."""
    fig = go.Figure()
    renderers = {
        "Animal Cell": render_animal_cell,
        "Plant Cell": render_plant_cell,
        "Bacterial Cell": render_bacterial_cell,
        "Fungal Cell": render_fungal_cell,
        "Protist Cell": render_protist_cell,
        "Neuron": render_neuron,
        "Red Blood Cell": render_red_blood_cell,
        "White Blood Cell": render_white_blood_cell,
    }
    renderers[profile.name](fig)
    fig.update_layout(
        height=620,
        margin={"l": 0, "r": 0, "t": 35, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        scene={
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.55, "y": 1.55, "z": 1.1}},
        },
        showlegend=False,
        title={"text": f"Realistic 3D labelled diagram: {profile.name}", "x": 0.5},
    )
    return fig


def render_student_card() -> None:
    details_html = "".join(f"<b>{key}:</b> {value}<br>" for key, value in STUDENT_DETAILS.items())
    st.sidebar.markdown(
        f"""
        <div class="student-card">
            <h3>Student Details</h3>
            {details_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz(profile: CellProfile) -> None:
    st.subheader(f"Quiz for {profile.name}")
    score = 0
    for index, question in enumerate(profile.quiz, start=1):
        response = st.radio(
            question.question,
            question.options,
            key=f"{profile.name}-{index}",
            index=None,
        )
        if response:
            if response == question.answer:
                score += 1
                st.success(f"Correct. {question.explanation}")
            else:
                st.error(f"Incorrect. Correct answer: {question.answer}. {question.explanation}")
    st.info(f"Current score for this cell: {score}/{len(profile.quiz)}")


def main() -> None:
    st.set_page_config(
        page_title="Introduction of Computational Biology",
        page_icon="🧬",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .main-title {font-size: 3rem; font-weight: 800; color: #0f766e;}
        .subtitle {font-size: 1.1rem; color: #334155;}
        .student-card {position: sticky; top: 1rem; padding: 1rem; border-radius: 1rem; background: linear-gradient(135deg, #ecfeff, #f0fdf4); border: 1px solid #99f6e4; box-shadow: 0 6px 18px rgba(15, 118, 110, 0.14);}
        .cell-chip {display: inline-block; padding: .25rem .65rem; border-radius: 999px; background: #e0f2fe; color: #075985; font-weight: 700; margin-bottom: .5rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    render_student_card()

    st.markdown('<div class="main-title">Introduction of Computational Biology</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">A public Streamlit learning website with biological cell theory, realistic 3D labelled diagrams, and quizzes for students.</p>',
        unsafe_allow_html=True,
    )

    st.write(
        "Computational biology combines biology, computer science, mathematics, and statistics to analyze living systems. "
        "This app presents representative biological cells and explains how computational methods help study their structure, function, and data."
    )

    selected_name = st.sidebar.selectbox("Choose a biological cell", [profile.name for profile in CELL_PROFILES])
    profile = next(cell for cell in CELL_PROFILES if cell.name == selected_name)

    left, right = st.columns([1.25, 1])
    with left:
        st.plotly_chart(build_cell_figure(profile), use_container_width=True)
    with right:
        st.markdown(f'<span class="cell-chip">{profile.kingdom}</span>', unsafe_allow_html=True)
        st.header(profile.name)
        st.write(profile.summary)
        st.subheader("Theory")
        for point in profile.theory:
            st.markdown(f"- {point}")
        st.subheader("Labels included")
        st.write(", ".join(profile.labels))

    st.divider()
    render_quiz(profile)

    st.divider()
    st.header("Complete cell theory overview")
    tabs = st.tabs([profile.name for profile in CELL_PROFILES])
    for tab, cell in zip(tabs, CELL_PROFILES, strict=True):
        with tab:
            st.subheader(cell.name)
            st.write(cell.summary)
            for point in cell.theory:
                st.markdown(f"- {point}")
            st.caption("Quiz is available by selecting this cell from the sidebar.")


if __name__ == "__main__":
    main()
