import streamlit as st
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt
from Bio import SeqIO
import io

# Page config
st.set_page_config(page_title='BioSequence Analyzer', page_icon='🧬')

# Title
st.title("🧬 BioSequence Analyzer")
st.write("Paste a DNA Sequence below to analyze it.")

# Input box
st.subheader("Input Sequence")
input_method = st.radio("Choose input method:", ["Paste Sequence", "Upload FASTA File"])
sequence_input = ""
sequence_name = "Manual Input"

if input_method == "Paste Sequence":
    sequence_input = st.text_area('Enter DNA Sequence', height=150, placeholder='e.g. ATGCGTACGTAGCTAGCTAGC')
elif input_method == "Upload FASTA File":
    uploaded_file = st.file_uploader("Upload a FASTA file:", type=['fasta', 'fa', 'txt'])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        records = list(SeqIO.parse(io.StringIO(content), "fasta"))
        if len(records) == 0:
            st.error("No Sequences found in file. Make sure it is valid Fasta File.")
        else:
            sequence_name = records[0].id
            sequence_input = str(records[0].seq)
            st.success(f"Loaded Sequence: {sequence_name}")
            st.code(sequence_input[:100] + "..." if len(sequence_input)>100 else sequence_input)

# Button
if st.button('Analyze'):
    if sequence_input.strip() == "":
        st.warning('Please enter sequence first.')
    else:
        seq = Seq(sequence_input.strip().upper())
        st.subheader("Basic Stats")
        col1, col2 = st.columns(2)
        
        col1.metric(label="Sequence length:", value=f"{len(seq)} bases.")
        col2.metric(label="GC Content:", value=f"{gc_fraction(seq) * 100:.2f}%")

        st.subheader("Reverse Complement")
        rev_comp = str(seq.reverse_complement())
        st.code(rev_comp)

        st.subheader("Transcription (DNA -> RNA)")
        rna = seq.transcribe()
        st.code(str(rna))

        st.subheader("Translation (RNA -> Protein)")
        protein = seq.translate()
        st.code(str(protein))

        st.subheader("Base Composition")

        bases = ["A", "T", "G", "C"]
        counts = [seq.count(b) for b in bases] 
        colors = ["#4CAF50", "#2196F3", "#FF5722", "#9C27B0"]
        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(bases, counts, color=colors)
        ax.set_xlabel("Base")
        ax.set_ylabel("Count")
        ax.set_title("Base Composition")
        for i, count in enumerate(counts):
            ax.text(i, count+0.2, str(count), ha="center", fontweight="bold")
        st.pyplot(fig)

        st.subheader("Download Report")
        report = f"""
        BioSequence Analyzer - Result Report

        Original Sequence: 
        {str(seq)}

        Basic Stats:
        Length: {len(seq)}
        GC Count: {gc_fraction(seq)*100:.2f}%

        Base Counts:
        A: {seq.count("A")}
        T: {seq.count("T")}
        G: {seq.count("G")}
        C: {seq.count("C")}

        Reverse Compliment:
        {rev_comp}

        Transcription (DNA -> RNA):
        {str(rna)}

        Translation (RNA -> Protein):
        {str(protein)}
        """

        st.download_button(
            label="Download Report as .txt",
            data=report,
            file_name="bio_report.txt",
            mime="text/plain"
        )