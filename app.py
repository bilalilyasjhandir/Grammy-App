import streamlit as st
import pandas as pd

#page configuration
st.set_page_config(
    page_title="Grammy Artist Lookup",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#css
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Background ── */
:root {
    --gold:    #C9A84C;
    --gold2:   #F0C040;
    --dark:    #0D0D0D;
    --card:    #161616;
    --border:  #2A2A2A;
    --text:    #E8E0D0;
    --muted:   #7A7068;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Hero Banner ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(201,168,76,0.18) 0%, transparent 70%);
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 4.2rem);
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--gold2) 0%, var(--gold) 50%, #a0742a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* ── Search box ── */
[data-testid="stTextInput"] input {
    background: #1A1A1A !important;
    border: 1.5px solid var(--gold) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 0.8rem 1.2rem !important;
    box-shadow: 0 0 24px rgba(201,168,76,0.12) !important;
    transition: box-shadow 0.3s ease;
}
[data-testid="stTextInput"] input:focus {
    box-shadow: 0 0 32px rgba(201,168,76,0.3) !important;
}
[data-testid="stTextInput"] label { color: var(--gold) !important; font-weight: 500 !important; font-size: 0.9rem !important; letter-spacing: 1px; text-transform: uppercase; }

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--gold2) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem !important;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gold);
    margin: 1.8rem 0 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* ── Artist name display ── */
.artist-name-display {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.artist-era-badge {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    border: 1px solid var(--gold);
    color: var(--gold);
    font-size: 0.78rem;
    font-weight: 500;
    padding: 2px 12px;
    border-radius: 999px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 2px;
}

/* ── Win badges ── */
.win-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.6rem;
}
.win-card-year { font-size: 0.78rem; color: var(--gold); font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
.win-card-category { font-size: 1rem; color: var(--text); font-weight: 500; margin: 2px 0; }
.win-card-title { font-size: 0.88rem; color: var(--muted); font-style: italic; }

/* ── Big Four badge ── */
.big-four-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), #a0742a);
    color: #000;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-left: 6px;
    vertical-align: middle;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── DataFrame ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.stDataFrame { background: var(--card) !important; }

/* ── Charts ── */
[data-testid="stVegaLiteChart"], [data-testid="stBarChart"], [data-testid="stLineChart"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* ── Top Artists Leaderboard ── */
.leaderboard-row {
    display: flex;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 0.5rem;
    gap: 1rem;
}
.lb-rank { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: var(--border); min-width: 32px; }
.lb-rank.top3 { color: var(--gold); }
.lb-artist { flex: 1; font-weight: 500; color: var(--text); }
.lb-wins { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: var(--gold2); min-width: 40px; text-align: right; }
.lb-wins-label { font-size: 0.7rem; color: var(--muted); text-align: right; }

/* ── Info/warning boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* ── Tabs ── */
[data-testid="stTab"] { color: var(--muted) !important; }
[aria-selected="true"] { color: var(--gold) !important; border-bottom-color: var(--gold) !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

#data
@st.cache_data
def load_data():
    winners  = pd.read_csv("C:\\Users\\BILAL\\BARAKODE\\Grammy-App\\data\\Grammy_Awards_Winners.csv",    encoding="utf-8-sig")
    big_four = pd.read_csv("C:\\Users\\BILAL\\BARAKODE\\Grammy-App\\data\\Grammy_Big_Four_Awards.csv",   encoding="utf-8-sig")
    top      = pd.read_csv("C:\\Users\\BILAL\\BARAKODE\\Grammy-App\\data\\Grammy_Top_Artists.csv",       encoding="utf-8-sig")
    decade   = pd.read_csv("C:\\Users\\BILAL\\BARAKODE\\Grammy-App\\data\\Grammy_Winners_By_Decade.csv", encoding="utf-8-sig")
    #normalise
    for df in [winners, big_four]:
        df.columns = [c.strip() for c in df.columns]
        df["Artist"]   = df["Artist"].astype(str).str.strip()
        df["Category"] = df["Category"].astype(str).str.strip()
        df["Winner"]   = df["Winner"].astype(str).str.strip()
        df["Year"]     = pd.to_numeric(df["Year"], errors="coerce")
    return winners, big_four, top, decade
winners, big_four, top_artists, decade_df = load_data()
#unique artists for autocomplete hint
all_artists = sorted(winners["Artist"].dropna().unique().tolist())

#hero
st.markdown("""
<div class="hero">
    <div class="hero-title">🏆 Grammy Award Lookup</div>
    <div class="hero-sub">1959 – 2026 · Explore every Grammy win across 68 ceremonies</div>
</div>
""", unsafe_allow_html=True)

#tabs
tab_search, tab_leaderboard, tab_decade = st.tabs(["🔍 Artist Search", "🥇 All-Time Leaderboard", "📅 Winners By Decade"])

#tab 1 - artist search
with tab_search:
    st.markdown("<br>", unsafe_allow_html=True)
    col_in, _ = st.columns([2, 1])
    with col_in:
        artist_input = st.text_input(
            "🎤 ARTIST NAME",
            placeholder="e.g. Adele, Taylor Swift, Kendrick Lamar…",
            help="Partial names work too — try 'Billie' or 'Paul'."
        )
    if not artist_input:
        #hint: show popular artists
        st.markdown("<div class='section-label'>Popular Artists in This Dataset</div>", unsafe_allow_html=True)
        hints = top_artists.head(10)
        cols = st.columns(5)
        for i, row in hints.iterrows():
            with cols[i % 5]:
                st.markdown(f"""
                <div style='background:#161616;border:1px solid #2A2A2A;border-radius:10px;
                            padding:0.8rem;text-align:center;margin-bottom:0.5rem;'>
                    <div style='font-size:0.78rem;color:#C9A84C;font-weight:600;
                                letter-spacing:0.5px;'>#{row['Rank']}</div>
                    <div style='font-weight:500;color:#E8E0D0;font-size:0.9rem;
                                margin:4px 0;'>{row['Artist']}</div>
                    <div style='font-family:"Playfair Display",serif;font-size:1.5rem;
                                color:#F0C040;'>{row['Total_Wins']}</div>
                    <div style='font-size:0.7rem;color:#7A7068;'>WINS</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        #case-insensitive partial match
        query = artist_input.strip()
        mask  = winners["Artist"].str.contains(query, case=False, na=False)
        artist_df = winners[mask].copy()
        if artist_df.empty:
            st.warning(f"No results found for **\"{query}\"**. Try a shorter name or check the spelling.")
        else:
            #get most common full artist matched
            top_name = artist_df["Artist"].value_counts().idxmax()
            exact_df = artist_df[artist_df["Artist"].str.lower() == top_name.lower()]
            if exact_df.empty:
                exact_df = artist_df  #fallback to all matches
            wins_df     = exact_df[exact_df["Status"] == "Winner"]
            big4_wins   = wins_df[wins_df["Award_Group"] == "Big Four"]
            genre_wins  = wins_df[wins_df["Award_Group"] == "Genre"]
            eras        = exact_df["Era"].dropna().unique().tolist()
            #artist header
            st.markdown(f"<div class='artist-name-display'>🎤 {top_name}</div>", unsafe_allow_html=True)
            for era in sorted(set(eras)):
                st.markdown(f"<span class='artist-era-badge'>{era}</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            #key metrics
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("🏆 Total Wins",        len(wins_df))
            m2.metric("⭐ Big Four Wins",      len(big4_wins))
            m3.metric("🎵 Genre Wins",         len(genre_wins))
            m4.metric("📅 First Win",
                      int(wins_df["Year"].min()) if not wins_df.empty else "—")
            m5.metric("📅 Last Win",
                      int(wins_df["Year"].max()) if not wins_df.empty else "—")
            st.markdown("<hr>", unsafe_allow_html=True)
            #wins section
            if wins_df.empty:
                st.info("No Grammy wins found for this artist in the dataset.")
            else:
                st.markdown("<div class='section-label'>🏆 Grammy Wins</div>", unsafe_allow_html=True)
                #top 4 wins first
                if not big4_wins.empty:
                    st.markdown("**Big Four Awards** &nbsp;<span class='big-four-badge'>PRESTIGIOUS</span>", unsafe_allow_html=True)
                    for _, row in big4_wins.sort_values("Year", ascending=False).iterrows():
                        st.markdown(f"""
                        <div class='win-card'>
                            <div class='win-card-year'>{int(row['Year'])} · Ceremony #{int(row['Ceremony_Number'])}</div>
                            <div class='win-card-category'>{row['Category']}</div>
                            <div class='win-card-title'>"{row['Winner']}"</div>
                        </div>
                        """, unsafe_allow_html=True)
                if not genre_wins.empty:
                    st.markdown("<br>**Genre & Specialty Awards**", unsafe_allow_html=True)
                    for _, row in genre_wins.sort_values("Year", ascending=False).iterrows():
                        st.markdown(f"""
                        <div class='win-card' style='border-left-color:#4a4a4a;'>
                            <div class='win-card-year'>{int(row['Year'])} · Ceremony #{int(row['Ceremony_Number'])}</div>
                            <div class='win-card-category'>{row['Category']}</div>
                            <div class='win-card-title'>"{row['Winner']}"</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            #charts
            if len(wins_df) > 1:
                st.markdown("<div class='section-label'>📊 Win Analysis</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Wins by Category**")
                    cat_counts = wins_df["Category"].value_counts().reset_index()
                    cat_counts.columns = ["Category", "Wins"]
                    st.bar_chart(cat_counts.set_index("Category"), color="#C9A84C")
                with c2:
                    st.markdown("**Wins Over the Years**")
                    year_wins = wins_df.groupby("Year").size().reset_index(name="Wins")
                    st.line_chart(year_wins.set_index("Year"), color="#F0C040")
            #category breakdown
            if not wins_df.empty:
                st.markdown("<div class='section-label'>📋 Full Win History</div>", unsafe_allow_html=True)
                display_df = wins_df[["Year", "Ceremony_Number", "Category", "Award_Group", "Winner", "Era"]]\
                    .sort_values("Year", ascending=False).reset_index(drop=True)
                display_df.columns = ["Year", "Ceremony #", "Category", "Award Group", "Song/Album", "Era"]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            #decade breakdown
            if not wins_df.empty and "Decade" in wins_df.columns:
                st.markdown("<div class='section-label'>🕐 Wins by Decade</div>", unsafe_allow_html=True)
                decade_wins = wins_df.groupby("Decade").size().reset_index(name="Wins")
                decade_wins["Decade"] = decade_wins["Decade"].astype(str) + "s"
                st.bar_chart(decade_wins.set_index("Decade"), color="#C9A84C")
            #other matching artist warning
            other = artist_df[artist_df["Artist"].str.lower() != top_name.lower()]["Artist"].unique()
            if len(other) > 0:
                st.info(f"Your search also matched: **{', '.join(other[:5])}**. Try a more specific name to filter them.")

#tab 2 - all time leaderboard
with tab_leaderboard:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>🥇 Top 20 Grammy Artists of All Time</div>", unsafe_allow_html=True)
    st.caption("Based on Big Four Grammy wins (Album, Record, Song of the Year & Best New Artist)")
    for _, row in top_artists.iterrows():
        rank = int(row["Rank"])
        is_top3 = "top3" if rank <= 3 else ""
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
        bar_pct = int((row["Total_Wins"] / top_artists["Total_Wins"].max()) * 100)
        st.markdown(f"""
        <div class='leaderboard-row'>
            <div class='lb-rank {is_top3}'>{medal}</div>
            <div style='flex:1;'>
                <div class='lb-artist'>{row['Artist']}</div>
                <div style='font-size:0.75rem;color:#7A7068;margin-top:2px;'>
                    {row['Sample_Categories']} · {int(row['First_Win_Year'])}–{int(row['Last_Win_Year'])}
                </div>
                <div style='margin-top:6px;background:#2A2A2A;border-radius:4px;height:4px;'>
                    <div style='width:{bar_pct}%;background:linear-gradient(90deg,#C9A84C,#F0C040);
                                border-radius:4px;height:4px;'></div>
                </div>
            </div>
            <div>
                <div class='lb-wins'>{int(row['Total_Wins'])}</div>
                <div class='lb-wins-label'>WINS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>📊 Wins Distribution</div>", unsafe_allow_html=True)
    chart_df = top_artists[["Artist","Total_Wins"]].set_index("Artist")
    st.bar_chart(chart_df, color="#C9A84C")

#tab 3 - winners by decade
with tab_decade:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>📅 Grammy Winners by Decade & Category</div>", unsafe_allow_html=True)
    #pivot table
    pivot = decade_df.pivot_table(
        index="Decade", columns="Category", values="Total_Winners", fill_value=0
    )
    pivot.index = [f"{int(d)}s" for d in pivot.index]
    st.dataframe(pivot, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>📊 Total Grammys Awarded Per Decade</div>", unsafe_allow_html=True)
    totals = decade_df.groupby("Decade")["Total_Winners"].sum().reset_index()
    totals["Decade"] = totals["Decade"].astype(str) + "s"
    st.bar_chart(totals.set_index("Decade"), color="#C9A84C")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>📈 Winners by Decade & Category (Stacked)</div>", unsafe_allow_html=True)
    st.dataframe(
        decade_df.sort_values(["Decade","Category"]).reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

#footer
st.markdown("""
<div class='footer'>
    Grammy Award Winners 1959–2026 · Data sourced from <a href='https://www.kaggle.com/datasets/mafaqbhatti/grammy-award-winners-1959-2026' target='_blank' style='color:#C9A84C;text-decoration:none;'>Kaggle</a><br>
</div>
""", unsafe_allow_html=True)