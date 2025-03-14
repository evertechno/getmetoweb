import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time
import plotly.graph_objects as go
import validators

# Function to extract SEO metrics from a webpage
def extract_seo_metrics(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_tag = soup.find('title').text if soup.find('title') else 'No Title Found'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else 'No Meta Description Found'
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        internal_links = [link['href'] for link in soup.find_all('a', href=True) if url in link['href']]
        external_links = [link['href'] for link in soup.find_all('a', href=True) if url not in link['href']]
        images = soup.find_all('img')
        alt_texts = [img.get('alt', 'No Alt Text') for img in images]
        canonical = soup.find('link', rel='canonical')
        canonical_link = canonical['href'] if canonical else 'No Canonical Link Found'
        favicon = soup.find('link', rel='icon')
        favicon_link = favicon['href'] if favicon else 'No Favicon Found'
        word_count = len(soup.get_text().split())
        structured_data = soup.find_all('script', type='application/ld+json')
        schema_org = [data.text for data in structured_data]
        open_graph = soup.find_all('meta', property=re.compile(r'^og'))
        twitter_cards = soup.find_all('meta', attrs={'name': re.compile(r'^twitter')})
        
        return {
            'title_tag': title_tag,
            'meta_description': meta_description_content,
            'h1_count': len(h1_tags),
            'h2_count': len(h2_tags),
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'image_count': len(images),
            'alt_texts': alt_texts,
            'canonical_link': canonical_link,
            'favicon_link': favicon_link,
            'word_count': word_count,
            'schema_org': schema_org,
            'open_graph': open_graph,
            'twitter_cards': twitter_cards
        }
    except Exception as e:
        return {'error': str(e)}

# Function to generate SEO health status
def seo_health_status(metrics):
    status = 'Good'
    if len(metrics['title_tag']) < 10 or len(metrics['title_tag']) > 60:
        status = 'Title Tag: Needs Improvement'
    elif len(metrics['meta_description']) < 50 or len(metrics['meta_description']) > 160:
        status = 'Meta Description: Needs Improvement'
    return status

# Function to plot a dynamic SEO performance graph
def plot_seo_performance(metrics):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['H1 Tags', 'H2 Tags', 'Internal Links', 'External Links', 'Images'],
        y=[metrics['h1_count'], metrics['h2_count'], metrics['internal_links'], metrics['external_links'], metrics['image_count']],
        name='SEO Metrics',
        marker_color=['#FF6347', '#FF4500', '#2E8B57', '#1E90FF', '#FFA07A']
    ))

    fig.update_layout(
        title="SEO Performance Overview",
        xaxis_title="SEO Elements",
        yaxis_title="Count",
        plot_bgcolor='rgb(255, 255, 255)',
        paper_bgcolor='rgb(240, 240, 240)',
        template="plotly_dark"
    )
    return fig

# Function to handle URL input and SEO audit
def seo_audit_tool():
    st.set_page_config(page_title="SEO Audit Tool", layout="wide", page_icon="🔍")
    
    # Title and Description
    st.title("SEO Audit Tool")
    st.write("### Enter the URL of your website for SEO analysis:")
    
    # URL input
    url = st.text_input("Enter URL:", "https://example.com")
    
    if st.button('Start SEO Audit'):
        if not validators.url(url):
            st.error("Invalid URL. Please enter a valid URL.")
        else:
            with st.spinner('Running SEO Audit...'):
                time.sleep(2)  # Simulating processing delay
                
                # Get SEO metrics
                metrics = extract_seo_metrics(url)
                
                if 'error' in metrics:
                    st.error(f"Error: {metrics['error']}")
                else:
                    # Display SEO metrics
                    st.subheader("SEO Analysis Results:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Title Tag:** {metrics['title_tag']}")
                        st.write(f"**Meta Description:** {metrics['meta_description']}")
                        st.write(f"**Number of H1 Tags:** {metrics['h1_count']}")
                        st.write(f"**Number of H2 Tags:** {metrics['h2_count']}")
                    with col2:
                        st.write(f"**Internal Links Count:** {metrics['internal_links']}")
                        st.write(f"**External Links Count:** {metrics['external_links']}")
                        st.write(f"**Image Count:** {metrics['image_count']}")
                        st.write(f"**Word Count:** {metrics['word_count']}")
                    
                    # SEO health status
                    seo_status = seo_health_status(metrics)
                    st.markdown(f"**SEO Health Status:** {seo_status}")
                    
                    # Display performance graph
                    st.plotly_chart(plot_seo_performance(metrics))

                    # SEO Improvement Suggestions
                    st.subheader("SEO Recommendations:")
                    if len(metrics['title_tag']) < 10 or len(metrics['title_tag']) > 60:
                        st.write("🔴 **Title Tag**: The title tag is too short or too long. Keep it between 10-60 characters.")
                    if len(metrics['meta_description']) < 50 or len(metrics['meta_description']) > 160:
                        st.write("🔴 **Meta Description**: The meta description is too short or too long. Keep it between 50-160 characters.")
                    if metrics['h1_count'] == 0:
                        st.write("🔴 **H1 Tag**: Make sure to include a single H1 tag on your page.")
                    if metrics['h2_count'] == 0:
                        st.write("🔴 **H2 Tags**: Consider adding H2 tags for better structure.")
                    if metrics['image_count'] == 0:
                        st.write("🔴 **Images**: Consider adding images to enhance content.")
                    if 'No Alt Text' in metrics['alt_texts']:
                        st.write("🔴 **Image Alt Text**: Some images are missing alt text. Add descriptive alt text to all images.")
                    if metrics['canonical_link'] == 'No Canonical Link Found':
                        st.write("🔴 **Canonical Link**: Consider adding a canonical link to prevent duplicate content issues.")
                    if metrics['favicon_link'] == 'No Favicon Found':
                        st.write("🔴 **Favicon**: Add a favicon to your website for better branding.")
                    if metrics['schema_org'] == []:
                        st.write("🔴 **Structured Data**: Consider adding structured data (Schema.org) to help search engines understand your content.")
                    if metrics['open_graph'] == []:
                        st.write("🔴 **Open Graph**: Add Open Graph meta tags to improve your website's integration with social media.")
                    if metrics['twitter_cards'] == []:
                        st.write("🔴 **Twitter Cards**: Add Twitter Card meta tags for better sharing on Twitter.")
                    st.write("✅ **Internal Links**: Keep a good balance of internal and external links.")
    
# Run the SEO Audit Tool
if __name__ == '__main__':
    seo_audit_tool()
