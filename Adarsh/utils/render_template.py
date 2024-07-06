from Adarsh.vars import Var
from Adarsh.bot import StreamBot
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import get_file_ids
from Adarsh.server.exceptions import InvalidHash
import urllib.parse
import aiofiles
import logging
import aiohttp


async def render_page(id, secure_hash):
    file_data = await get_file_ids(StreamBot, int(Var.BIN_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash
    
    src = urllib.parse.urljoin(Var.URL, f'{secure_hash}{str(id)}')
    current_url = f'{Var.URL}/{str(id)}/{file_data.file_name}?hash={secure_hash}'

    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = f'Watch {file_data.file_name}'
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = f'Listen {file_data.file_name}'
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    else:
        async with aiofiles.open('Adarsh/template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(src) as u:
                    heading = f'Download {file_data.file_name}'
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, src, file_size)

    html_code = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{heading}</title>
        <style>
            body {{
                font-family: "Arial Black", sans-serif;
                background-color: #2c2c2c;
                color: #fff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                padding: 0 20px; /* Added padding for better layout */
            }}
            h5 {{
                color: #ddd;
                margin-bottom: 20px;
                text-align: center; /* Center text */
            }}
            .button-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                max-width: 400px; /* Adjust max-width as needed */
                margin-top: 20px; /* Added margin */
            }}
            .button-container button {{
                font-size: 16px;
                margin: 8px;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                align-items: center;
                transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
                color: #fff;
                font-weight: bold;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                background-image: linear-gradient(
                    45deg,
                    rgba(255, 255, 255, 0.2) 50%,
                    transparent 50%
                );
                background-size: 200% 200%;
                transition: background-position 0.5s;
                width: 100%; /* Full width for buttons */
            }}
            .button-container button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
                opacity: 0.9;
                background-position: 100%;
            }}
            .button-container img {{
                margin-right: 8px;
                width: 26px;
                height: 26px;
            }}
            .mx-button {{
                background-color: #0088cc; /* Telegram Blue */
            }}
            .vlc-button {{
                background-color: #ff8f00; /* Orange */
            }}
            .playit-button {{
                background-color: #d32f2f; /* Red */
            }}
            .save-button {{
                background-color: #673ab7; /* Purple */
            }}
            .telegram-button {{
                background-color: #009688; /* Teal */
            }}
            .playit-button + .save-button {{
                margin-top: 24px; /* Increased gap */
            }}

            @media screen and (max-width: 600px) {{
                .button-container {{
                    max-width: 300px; /* Adjust for smaller screens */
                }}
                .button-container button {{
                    font-size: 14px; /* Decrease font size further */
                }}
            }}
        </style>
    </head>
    <body>
        <h5>{heading}</h5> <!-- Display heading here -->
        <div class="button-container">
            <button class="mx-button" onclick="window.location.href = 'intent:{current_url}#Intent;package=com.mxtech.videoplayer.ad;S.title={file_data.file_name};end'">
                WATCH IN MX PLAYER
            </button>
            <button class="vlc-button" onclick="window.location.href = 'vlc://{current_url}'">
                WATCH IN VLC PLAYER
            </button>
            <button class="playit-button" onclick="window.location.href = 'playit://playerv2/video?url={current_url}&amp;title={file_data.file_name}'">
                WATCH IN PLAYIT PLAYER
            </button>
            <button class="save-button" onclick="window.location.href = '{current_url}'">
                DOWNLOAD FILE
            </button>
            <button class="telegram-button" onclick="window.location.href = 'https://telegram.me/RahulReviewsYT'">
                JOIN ON TELEGRAM
            </button>
        </div>
    </body>
    </html>
    '''

    return html + html_code
