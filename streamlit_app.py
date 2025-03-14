import streamlit as st
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import re

def check_meta_tags(soup):
    meta_tags = {
        "title": soup.title.string if soup.title else "Missing",
        "description": "Missing",
        "keywords": "Missing",
        "viewport": "Missing"
    }
    for tag in soup.find_all("meta"):
        if tag.get("name") == "description":
            meta_tags["description"] = tag.get("content", "Missing")
        elif tag.get("name") == "keywords":
            meta_tags["keywords"] = tag.get("content", "Missing")
        elif tag.get("name") == "viewport":
            meta_tags["viewport"] = tag.get("content", "Missing")
    return meta_tags

def check_headings(soup):
    headings = {
        "h1": len(soup.find_all("h1")),
        "h2": len(soup.find_all("h2")),
        "h3": len(soup.find_all("h3")),
        "h4": len(soup.find_all("h4")),
        "h5": len(soup.find_all("h5")),
        "h6": len(soup.find_all("h6"))
    }
    return headings

def check_images(soup):
    images = {
        "total_images": len(soup.find_all("img")),
        "missing_alt": len([img for img in soup.find_all("img") if not img.get("alt")])
    }
    return images

def check_links(soup):
    links = {
        "total_links": len(soup.find_all("a")),
        "internal_links": len([a for a in soup.find_all("a") if a.get("href", "").startswith("/")]),
        "external_links": len([a for a in soup.find_all("a") if a.get("href", "").startswith("http")])
    }
    return links

def check_load_time(url):
    response = requests.get(url)
    load_time = response.elapsed.total_seconds()
    return load_time

def check_word_count(soup):
    text = soup.get_text()
    word_count = len(text.split())
    return word_count

def check_keyword_density(soup, keyword):
    text = soup.get_text().lower()
    keyword_count = text.count(keyword.lower())
    total_words = len(text.split())
    density = (keyword_count / total_words) * 100 if total_words > 0 else 0
    return density

def check_mobile_friendly(soup):
    viewport_tag = soup.find("meta", {"name": "viewport"})
    return "Yes" if viewport_tag else "No"

def check_ssl(url):
    return "Yes" if url.startswith("https") else "No"

def check_broken_links(soup, url):
    broken_links = []
    for a in soup.find_all("a"):
        link = a.get("href")
        if link and link.startswith("http"):
            try:
                response = requests.head(link)
                if response.status_code >= 400:
                    broken_links.append(link)
            except requests.RequestException:
                broken_links.append(link)
    return broken_links

def check_sitemap(url):
    sitemap_url = url.rstrip("/") + "/sitemap.xml"
    response = requests.head(sitemap_url)
    return "Present" if response.status_code == 200 else "Missing"

def check_robots_txt(url):
    robots_txt_url = url.rstrip("/") + "/robots.txt"
    response = requests.head(robots_txt_url)
    return "Present" if response.status_code == 200 else "Missing"

def check_canonical_tags(soup):
    canonical_tag = soup.find("link", {"rel": "canonical"})
    return canonical_tag.get("href") if canonical_tag else "Missing"

def check_favicon(soup):
    favicon = soup.find("link", {"rel": "icon"})
    return favicon.get("href") if favicon else "Missing"

def check_social_media_tags(soup):
    social_media_tags = {
        "og:title": "Missing",
        "og:description": "Missing",
        "og:image": "Missing",
        "twitter:card": "Missing",
        "twitter:title": "Missing",
        "twitter:description": "Missing",
        "twitter:image": "Missing"
    }
    for tag in soup.find_all("meta"):
        if tag.get("property") == "og:title":
            social_media_tags["og:title"] = tag.get("content", "Missing")
        elif tag.get("property") == "og:description":
            social_media_tags["og:description"] = tag.get("content", "Missing")
        elif tag.get("property") == "og:image":
            social_media_tags["og:image"] = tag.get("content", "Missing")
        elif tag.get("name") == "twitter:card":
            social_media_tags["twitter:card"] = tag.get("content", "Missing")
        elif tag.get("name") == "twitter:title":
            social_media_tags["twitter:title"] = tag.get("content", "Missing")
        elif tag.get("name") == "twitter:description":
            social_media_tags["twitter:description"] = tag.get("content", "Missing")
        elif tag.get("name") == "twitter:image":
            social_media_tags["twitter:image"] = tag.get("content", "Missing")
    return social_media_tags

def check_schema_markup(soup):
    schema_markup = soup.find_all("script", {"type": "application/ld+json"})
    return "Present" if schema_markup else "Missing"

def check_image_optimization(soup):
    optimized_images = 0
    total_images = len(soup.find_all("img"))
    for img in soup.find_all("img"):
        if img.get("src") and (img.get("src").endswith(".jpg") or img.get("src").endswith(".png")):
            optimized_images += 1
    return f"{optimized_images}/{total_images}"

def check_internal_link_structure(soup):
    internal_links = [a.get("href") for a in soup.find_all("a") if a.get("href", "").startswith("/")]
    return internal_links

def check_header_response(url):
    response = requests.head(url)
    return response.status_code

def check_structured_data(soup):
    structured_data = soup.find_all("script", {"type": "application/ld+json"})
    return "Present" if structured_data else "Missing"

def check_amp(soup):
    amp = soup.find("link", {"rel": "amphtml"})
    return amp.get("href") if amp else "Missing"

def check_breadcrumbs(soup):
    breadcrumbs = soup.find("nav", {"aria-label": "breadcrumb"})
    return "Present" if breadcrumbs else "Missing"

def check_page_depth(soup):
    depth = len(soup.find_all("a", href=True))
    return depth

def check_url_length(url):
    return len(url)

def check_hreflang_tags(soup):
    hreflang_tags = soup.find_all("link", {"rel": "alternate", "hreflang": True})
    return [tag.get("hreflang") for tag in hreflang_tags]

def check_noindex_tags(soup):
    noindex = soup.find("meta", {"name": "robots", "content": "noindex"})
    return "Present" if noindex else "Missing"

def check_nofollow_tags(soup):
    nofollow = soup.find("meta", {"name": "robots", "content": "nofollow"})
    return "Present" if nofollow else "Missing"

def check_content_security_policy(soup):
    csp = soup.find("meta", {"http-equiv": "Content-Security-Policy"})
    return csp.get("content") if csp else "Missing"

def check_http2(url):
    response = requests.get(url)
    return response.raw.version == 2

def check_font_size(soup):
    styles = soup.find_all("style")
    font_sizes = []
    for style in styles:
        sizes = re.findall(r'font-size:\s*(\d+px)', style.get_text())
        font_sizes.extend(sizes)
    return font_sizes

def check_color_contrast(soup):
    styles = soup.find_all("style")
    color_contrasts = []
    for style in styles:
        contrasting_colors = re.findall(r'color:\s*(#[0-9a-fA-F]{6})', style.get_text())
        color_contrasts.extend(contrasting_colors)
    return color_contrasts

def create_radar_chart(labels, values, title):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='red', alpha=0.25)
    ax.plot(angles, values, color='red', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(title, size=20, color='red', y=1.1)
    return fig

st.set_page_config(page_title="SEO Audit Tool", page_icon=":mag:", layout="wide")
st.title("SEO Audit Tool")
st.markdown("This tool performs a comprehensive SEO audit of a given webpage. Enter the URL below to get started.")

url = st.text_input("Enter URL", "https://example.com")

if st.button("Audit"):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    st.header("Meta Tags")
    meta_tags = check_meta_tags(soup)
    st.write(meta_tags)
    
    st.header("Headings")
    headings = check_headings(soup)
    st.write(headings)
    
    st.header("Images")
    images = check_images(soup)
    st.write(images)
    
    st.header("Links")
    links = check_links(soup)
    st.write(links)
    
    st.header("Load Time")
    load_time = check_load_time(url)
    st.write(f"{load_time} seconds")
    
    st.header("Word Count")
    word_count = check_word_count(soup)
    st.write(word_count)
    
    keyword = st.text_input("Enter Keyword for Density Check", "example")
    if keyword:
        st.header("Keyword Density")
        density = check_keyword_density(soup, keyword)
        st.write(f"{density}%")
    
    st.header("Mobile-Friendliness")
    mobile_friendly = check_mobile_friendly(soup)
    st.write(mobile_friendly)
    
    st.header("SSL Certificate")
    ssl = check_ssl(url)
    st.write(ssl)
    
    st.header("Broken Links")
    broken_links = check_broken_links(soup, url)
    st.write(broken_links)
    
    st.header("Sitemap Presence")
    sitemap = check_sitemap(url)
    st.write(sitemap)
    
    st.header("Robots.txt Presence")
    robots_txt = check_robots_txt(url)
    st.write(robots_txt)
    
    st.header("Canonical Tags")
    canonical_tags = check_canonical_tags(soup)
    st.write(canonical_tags)
    
    st.header("Favicon Presence")
    favicon = check_favicon(soup)
    st.write(favicon)
    
    st.header("Social Media Tags")
    social_media_tags = check_social_media_tags(soup)
    st.write(social_media_tags)
    
    st.header("Schema Markup")
    schema_markup = check_schema_markup(soup)
    st.write(schema_markup)
    
    st.header("Image Optimization")
    image_optimization = check_image_optimization(soup)
    st.write(image_optimization)
    
    st.header("Internal Link Structure")
    internal_link_structure = check_internal_link_structure(soup)
    st.write(internal_link_structure)
    
    st.header("Header Response")
    header_response = check_header_response(url)
    st.write(header_response)
    
    st.header("Structured Data")
    structured_data = check_structured_data(soup)
    st.write(structured_data)
    
    st.header("AMP")
    amp = check_amp(soup)
    st.write(amp)
    
    st.header("Breadcrumbs")
    breadcrumbs = check_breadcrumbs(soup)
    st.write(breadcrumbs)
    
    st.header("Page Depth")
    page_depth = check_page_depth(soup)
    st.write(page_depth)
    
    st.header("URL Length")
    url_length = check_url_length(url)
    st.write(url_length)
    
    st.header("Hreflang Tags")
    hreflang_tags = check_hreflang_tags(soup)
    st.write(hreflang_tags)
    
    st.header("NoIndex Tags")
    noindex_tags = check_noindex_tags(soup)
    st.write(noindex_tags)
    
    st.header("NoFollow Tags")
    nofollow_tags = check_nofollow_tags(soup)
    st.write(nofollow_tags)
    
    st.header("Content Security Policy")
    content_security_policy = check_content_security_policy(soup)
    st.write(content_security_policy)
    
    st.header("HTTP/2")
    http2 = check_http2(url)
    st.write(http2)
    
    st.header("Font Size")
    font_sizes = check_font_size(soup)
    st.write(font_sizes)
    
    st.header("Color Contrast")
    color_contrasts = check_color_contrast(soup)
    st.write(color_contrasts)
    
    st.header("SEO Radar Chart")
    radar_labels = ["Meta Tags", "Headings", "Images", "Links", "Load Time", "Word Count", "Keyword Density",
                    "Mobile-Friendliness", "SSL", "Broken Links", "Sitemap", "Robots.txt", "Canonical Tags", 
                    "Favicon", "Social Media Tags", "Schema Markup", "Image Optimization", "Internal Links",
                    "Header Response", "Structured Data", "AMP", "Breadcrumbs", "Page Depth", "URL Length",
                    "Hreflang Tags", "NoIndex Tags", "NoFollow Tags", "Content Security Policy", "HTTP/2",
                    "Font Size", "Color Contrast"]
    radar_values = [
        len(meta_tags),
        sum(headings.values()),
        images["total_images"],
        links["total_links"],
        1 / load_time if load_time > 0 else 0,
        word_count,
        density,
        1 if mobile_friendly == "Yes" else 0,
        1 if ssl == "Yes" else 0,
        len(broken_links),
        1 if sitemap == "Present" else 0,
        1 if robots_txt == "Present" else 0,
        1 if canonical_tags != "Missing" else 0,
        1 if favicon != "Missing" else 0,
        sum(1 for tag in social_media_tags.values() if tag != "Missing"),
        1 if schema_markup == "Present" else 0,
        int(image_optimization.split("/")[0]),
        len(internal_link_structure),
        header_response,
        1 if structured_data == "Present" else 0,
        1 if amp != "Missing" else 0,
        1 if breadcrumbs == "Present" else 0,
        page_depth,
        url_length,
        len(hreflang_tags),
        1 if noindex_tags == "Present" else 0,
        1 if nofollow_tags == "Present" else 0,
        1 if content_security_policy != "Missing" else 0,
        1 if http2 else 0,
        len(font_sizes),
        len(color_contrasts)
    ]
    radar_fig = create_radar_chart(radar_labels, radar_values, "SEO Audit Summary")
    st.pyplot(radar_fig)
    
    st.markdown("---")
    st.markdown("### Additional Features")
    st.markdown("1. Mobile-Friendliness Check")
    st.markdown("2. SSL Certificate Check")
    st.markdown("3. Broken Links Check")
    st.markdown("4. Sitemap Presence Check")
    st.markdown("5. Robots.txt Presence Check")
    st.markdown("6. Canonical Tags Check")
    st.markdown("7. Favicon Presence Check")
    st.markdown("8. Social Media Tags Check")
    st.markdown("9. Schema Markup Check")
    st.markdown("10. Page Speed Insights Integration")
    st.markdown("11. Image Optimization Check")
    st.markdown("12. Internal Link Structure Check")
    st.markdown("13. Header Response Check")
    st.markdown("14. Structured Data Check")
    st.markdown("15. AMP Check")
    st.markdown("16. Breadcrumbs Check")
    st.markdown("17. Page Depth Check")
    st.markdown("18. URL Length Check")
    st.markdown("19. Hreflang Tags Check")
    st.markdown("20. NoIndex Tags Check")
    st.markdown("21. NoFollow Tags Check")
    st.markdown("22. Content Security Policy Check")
    st.markdown("23. HTTP/2 Check")
    st.markdown("24. Font Size Check")
    st.markdown("25. Color Contrast Check")
