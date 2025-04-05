import streamlit as st
import re
from graphviz import Digraph

st.set_page_config(page_title="AI Meeting Process Visualizer", layout="wide")

st.title("🧠 FlowSense AI – Demo MVP (Offline)")
st.subheader("Simulazione del comportamento AI senza chiamate API")

st.markdown("### 📝 Transcript Esempio")
transcript = """
Marco (Business Owner): Abbiamo un problema con le richieste d'acquisto: spesso partono prima che il contratto sia stato approvato.
Laura (Procurement): Esatto, succede che la PR venga agganciata a un contratto non ancora firmato. Questo causa blocchi in accounting.
Giulia (Legal): Serve una validazione legale prima della creazione della PR se c'è un contratto.
Marco: In futuro vorrei che il processo fosse più automatico, magari con una validazione smart del contratto.
Laura: Potremmo inserire un check automatico che verifica se il contratto è approvato prima di far partire la PR.
Giulia: E magari anche un reminder al team legal se il contratto è fermo da più di 3 giorni.
"""
st.code(transcript)

if st.button("🔍 Simula Visualizzazione e Analisi"):
    with st.spinner("Elaborazione in corso..."):

        # Dati simulati per visualizzazione demo offline
        as_is_steps = [
            "Business crea PR",
            "PR agganciata a contratto",
            "Contratto non ancora firmato",
            "Blocco in accounting"
        ]

        to_be_steps = [
            "Check automatico contratto approvato?",
            "Notifica a Legal (se no)",
            "Creazione PR (se sì)",
            "Allineamento Accounting"
        ]

        pain_list = [
            "La PR può partire prima dell'approvazione contrattuale",
            "Rischi legali e contabili in caso di contratto incompleto",
            "Mancanza di sincronizzazione tra Legal e Procurement"
        ]

        st.markdown("### 🔁 As-Is Process")
        dot_as_is = Digraph()
        for i, step in enumerate(as_is_steps):
            dot_as_is.node(f"a{i}", step)
            if i > 0:
                dot_as_is.edge(f"a{i-1}", f"a{i}")
        st.graphviz_chart(dot_as_is)

        st.markdown("### 🚀 To-Be Process")
        dot_to_be = Digraph()
        for i, step in enumerate(to_be_steps):
            dot_to_be.node(f"b{i}", step)
            if i > 0:
                dot_to_be.edge(f"b{i-1}", f"b{i}")
        st.graphviz_chart(dot_to_be)

        st.markdown("### ⚠️ Pain Points & Insights")
        for p in pain_list:
            st.markdown(f"- {p}")
