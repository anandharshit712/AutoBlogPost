import os

output_dir = "generated_blogs"
os.makedirs(output_dir, exist_ok=True)

def save_blog_as_html(title, content, image_path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <img src="{image_path}" alt="Blog Image" style="width:100%;max-width:600px;">
        <div>
            <p>{content.replace('\n', '<br>')}</p>
        </div>
    </body>
    </html>
    """
    file_path = os.path.join(output_dir, "blog_post.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Blog post saved at: {file_path}")
