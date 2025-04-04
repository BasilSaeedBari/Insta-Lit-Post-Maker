from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Configurations
canvas_size = (1080, 1080)
background_image_path = 'background.jpg'  # Change as needed
font_path = 'font.ttf'  # Update with your font file
text_color = "black"
header_height = 50
footer_height = 15
footer_text = "@BasilWhoLived"

# Font Sizes (Customizable)
font_body_size = 35   # Font size for main body text
font_header_size = 25  # Font size for page number
font_footer_size = 22  # Font size for footer text
line_spacing = 8  # Space between lines (customizable)

# Margins and layout
top_margin = 90  # Space for page number
bottom_margin = 115  # Space for footer
side_margin = 50  # Left & right padding
text_area_height = canvas_size[1] - top_margin - bottom_margin  # Usable height for text

# Load fonts
font_body = ImageFont.truetype(font_path, font_body_size)
font_header = ImageFont.truetype(font_path, font_header_size)
font_footer = ImageFont.truetype(font_path, font_footer_size)

# Sample literature text
full_text = """He stands before me, myself. His eyes, sharp with knowing, his voice thick with the exhaustion of someone who has seen too much, thought too much, understood too much.
“I’m done,” he says. “I give up. The world as it is—bad, useless. All the effort I put in isn’t worth it. What do I do? I’m lost.”
I say nothing. At first.
The silence stretches between us like an abyss, unspoken yet immense. I have spent eons in silence, searching for something—anything—that was truly new. And I have failed. Every thought, every profound revelation, has already been whispered by another. Every path I have walked has been traced by countless footsteps before mine. The one before me knows this too, for he is me. We would see through the obvious answers. He would tear apart anything I offered. So I do not offer comfort. I do not offer wisdom. I offer only the truth, the truth I wanted to hear.
“You are lost,” I finally say, “because you are waiting for something that does not exist—a reason grand enough to make everything worth it. But there isn’t one. The world will hand you not meaning. Your mind will conjure not a final answer. There is no answer. Only the choice to move. And you—knowing everything—should know this: even if nothing matters, even if it is all useless, the act of choosing still remains yours. So choose something. Anything. And move.”
I turn from myself. Fleeting away. Knowing already that he wont follow but it is already happened so no longer is it my concern.
But myself changes reality. He shouts, does what I didn’t do before;
“AH, NIHILISM! ABSURDISM! THAT’S YOUR ANSWER?” My voice cracks, filled with fury. “I KNEW IT! YOU DIDN’T HAVE AN ORIGINAL THOUGHT! YOU’RE NOTHING BUT A COPY OF ALL PHILOSOPHY! THIS IS THE WE WALKED! A THIEF OF IDEAS! ANSWER ME! ”
The Angel of Death stops. The chains pull me. The world of limbo falls in silence.
A slow breath. Then, I laugh. Not mockingly. Not cruelly. Just a quiet, knowing laugh. I turn to myself.
“And what are you?” I ask.
Myself freezes, as the question echo beyond time.
“You knew my answer before I spoke it. You knew the weight of my words before they were even formed. You see through everything and find it lacking. So tell me—what is it you wanted? What answer could I give that you would not dismiss? What thought could I think that you would not recognize?”
I try to take a step forward, but the chains bind me, the angel weakens. Myself does not move.
“You think me a thief?” says the anger within I, heavy enough to break the chains but calm enough to break limbo into darkness. “Then let me steal something else from you—your certainty. You are lost not because the world is meaningless, but because you refuse to choose a meaning. Not because I am unoriginal, but because you refuse to be surprised. You claim to know all things, but the only thing you truly know is how to dismantle. You break everything down until nothing remains, and then you mourn the emptiness.”
Silence emerges as the angel falls.
“But tell me, child—when was the last time you built?”
I turn. I walk away to my destination leaving behind myself.
The angel rises, looks at myself and proclaims “The worlds do not wait for those who refuse to move.”
The angel looks up, shocked, not for I have walked centuries, but for myself is still there."""

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=100)  # Rough wrapping
        for line in wrapped:
            words = line.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                bbox = font.getbbox(test_line)
                if bbox[2] <= max_width:  # bbox[2] is the text width
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        lines.append("")  # Add blank line for paragraph spacing
    return lines

wrapped_lines = wrap_text(full_text, font_body, canvas_size[0] - 2 * side_margin)

# Get line height using font metrics
_, _, _, line_height = font_body.getbbox("A")  # More accurate than getsize()
total_line_height = line_height + line_spacing  # Includes custom spacing

# Compute number of lines per page
lines_per_page = text_area_height // total_line_height

# Split text into pages
pages = [wrapped_lines[i:i + lines_per_page] for i in range(0, len(wrapped_lines), lines_per_page)]

# Create output folder
os.makedirs("output_posts", exist_ok=True)

# Generate images for each page

for page_num, lines in enumerate(pages, start=1):
    img = Image.open(background_image_path).resize(canvas_size)
    draw = ImageDraw.Draw(img)

    # Draw page number (top-right)
    page_text = f"[{page_num}]"
    page_bbox = font_header.getbbox(page_text)
    draw.text((canvas_size[0] - page_bbox[2] - side_margin, header_height), page_text, font=font_header, fill=text_color)

    # Draw the text
    y_text = top_margin
    for line in lines:
        draw.text((side_margin, y_text), line, font=font_body, fill=text_color)
        y_text += total_line_height  # Use spacing

    # Draw footer (bottom-center)
    footer_bbox = font_footer.getbbox(footer_text)
    draw.text(((canvas_size[0] - footer_bbox[2]) / 2, canvas_size[1] - bottom_margin + footer_height),
              footer_text, font=font_footer, fill=text_color)

    # Save the image
    img.save(f"output_posts/post_{page_num}.png")

print(f"Generated {len(pages)} posts in 'output_posts' folder.")