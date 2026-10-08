import re

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix LLM key
text = text.replace('settings.GEMINI_API_KEY', 'settings.gemini_api_key')

# Enhance Chart
old_chart = '''        # Sparse x-ticks if there are many sessions
        tick_interval = max(1, len(x_axis) // 10)
        plt.xticks(x_axis[::tick_interval])
        
        plt.yticks([1, 2, 3], ['Low/Worse', 'Neutral', 'High/Better'])
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.savefig(chart_path, dpi=200)
        plt.close()'''

new_chart = '''        # Sparse x-ticks if there are many sessions
        tick_interval = max(1, len(x_axis) // 10)
        plt.xticks(x_axis[::tick_interval])
        
        plt.yticks([1, 2, 3], ['Low / Worse', 'Neutral / No Change', 'High / Better'])
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Calculate top topics for annotation
        all_topics = []
        for r in reviews:
            if r.topics:
                if isinstance(r.topics, list):
                    all_topics.extend(r.topics)
                elif isinstance(r.topics, str):
                    all_topics.extend([t.strip() for t in r.topics.split(',')])
                    
        if all_topics:
            from collections import Counter
            top_topics = [t[0] for t in Counter(all_topics).most_common(4)]
            topic_str = "Frequent Session Themes:\\n" + "\\n".join([f"- {t}" for t in top_topics])
            # Add text box to the chart clarifying the words/themes inside the sessions
            plt.text(1.02, 0.5, topic_str, transform=plt.gca().transAxes,
                     fontsize=10, verticalalignment='center',
                     bbox=dict(boxstyle='round', facecolor='#F3E8D6', alpha=0.8, edgecolor='#CA7C50'))
            
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
        plt.tight_layout(rect=[0, 0.05, 0.75, 1])
        plt.savefig(chart_path, dpi=200, bbox_inches='tight')
        plt.close()'''

text = text.replace(old_chart, new_chart)

with open(r'd:\NADABRAHMA\backend\app\routers\me.py', 'w', encoding='utf-8') as f:
    f.write(text)
