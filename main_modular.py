from extract_from_web import extract_topic_from_url
from generate_topic import generate_blog_title
from generate_content import generate_blog_content
from generate_image_prompt import generate_blog_content as generate_image_prompt
from generate_image import generate_image
from save_blog import save_blog_as_html


def main():
    news_url = "https://news.google.com/search?q=fitness"

    print("Extracting topic from news site...")
    topic = extract_topic_from_url(news_url)

    print("Generating blog title...")
    blog_title = generate_blog_title(topic, news_url)

    print("Generating blog content...")
    blog_content = generate_blog_content(blog_title)

    print("Generating image prompt...")
    image_prompt = generate_image_prompt(blog_content)

    print("Generating image...")
    image_path = generate_image(image_prompt)

    print(f"Blog creation process completed. Image saved at: {image_path}")

    save_blog_as_html(blog_title, blog_content, image_path)


if __name__ == "__main__":
    main()
