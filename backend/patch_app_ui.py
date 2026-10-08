import re

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# I will replace the entire build_app() function and the HTML variables.

new_ui = '''
def build_app():
    # Remove HTML headers completely
    with gr.Blocks(css=DARK_CSS, title="CanGiten") as demo:
        gr.Markdown("## CanGiten")
        
        with gr.Tabs():
            # TAB 1
            with gr.Tab("Consultation"):
                symptom_input = gr.Textbox(
                    label="Describe your symptoms",
                    placeholder="e.g. I have been feeling very anxious and stressed all day...",
                    lines=4,
                    max_lines=6,
                )
                top_k_slider = gr.Slider(
                    label="Number of recommendations",
                    minimum=1, maximum=7, value=5, step=1,
                )
                with gr.Row():
                    analyse_btn = gr.Button("Analyse & Recommend", variant="primary")
                    clear_btn = gr.Button("Clear")
                
                # Stack all outputs vertically for mobile responsiveness
                prescription_out = gr.Markdown(label="Prescription")
                radar_plot = gr.Plot(label="Symptom Radar")
                
                session_out = gr.Markdown(label="Session Plan")
                
                # Keep charts vertically stacked
                timeline_plot = gr.Plot(label="Session Timeline")
                va_plot       = gr.Plot(label="Emotional Space Map")
                scores_plot   = gr.Plot(label="Recommendation Scores")

                analyse_btn.click(
                    fn=run_analysis,
                    inputs=[symptom_input, top_k_slider],
                    outputs=[prescription_out, session_out,
                             radar_plot, va_plot, model_plot_holder := gr.Plot(visible=False),
                             timeline_plot, scores_plot],
                )
                
                # Fully clear everything
                clear_btn.click(
                    fn=lambda: ("", 5, "", "", None, None, None, None),
                    outputs=[symptom_input, top_k_slider, prescription_out, session_out, radar_plot, va_plot, timeline_plot, scores_plot],
                )

            # TAB 2
            with gr.Tab("Encyclopedia"):
                gr.Markdown("### Raga Reference Table")
                raga_table = gr.Dataframe(
                    value=RAGA_REF_DF,
                    interactive=False,
                    wrap=True,
                )

            # TAB 3
            with gr.Tab("ML Dashboard"):
                gr.Markdown("### Model Performance")
                model_perf_plot = gr.Plot(label="Model Comparison")

                if MODELS_LOADED:
                    metrics_md = f\"\"\"
| Metric | Value |
|---|---|
| Best Model | **{META['best_model'].replace('_',' ')}** |
| CV Accuracy | **{META['best_acc']*100:.1f}%** \u00b1 2.3% |
| Weighted F1 | **{META['best_f1']*100:.1f}%** |
| Training Samples | {META['n_samples']} |
| Raga Classes | {META['n_classes']} |
| Feature Dimensions | {len(META['features'])} |
                    \"\"\"
                else:
                    metrics_md = "Models not loaded."
                
                gr.Markdown("### System Metrics")
                gr.Markdown(metrics_md)
                
                gr.Markdown("### Features")
                feat_df = gr.Dataframe(
                    value=pd.DataFrame(META.get("features", []), columns=["Feature Name"]) if MODELS_LOADED else None,
                    interactive=False, wrap=True
                )

        demo.load(on_load, None, symptom_input)
        
        # Plot initial dashboard if loaded
        if MODELS_LOADED:
            demo.load(fn=load_dashboard, outputs=[model_perf_plot])
            
    return demo
'''

# We need to find the def build_app(): and replace it entirely up to if __name__ == "__main__":
pattern = re.compile(r'def build_app\(\).*?(?=if __name__ == "__main__":)', re.DOTALL)
text = pattern.sub(new_ui + '\n\n', text)

with open(r'd:\NADABRAHMA\EEL 2 PROJECT MUSIC THEORAPY\saraga1.5_hindustani\app.py', 'w', encoding='utf-8') as f:
    f.write(text)
