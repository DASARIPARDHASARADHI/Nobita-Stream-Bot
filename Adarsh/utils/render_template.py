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

    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = 'Watch {}'.format(file_data.file_name)
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = 'Listen {}'.format(file_data.file_name)
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src)
    else:
        async with aiofiles.open('Adarsh/template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(src) as u:
                    heading = 'Download {}'.format(file_data.file_name)
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, src, file_size)

    current_url = f'{Var.URL}/{str(id)}/{file_data.file_name}?hash={secure_hash}'

    html_code = f'''
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Download/Watch Video</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #2c2c2c;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
          }}
          h5 {{
            color: #ddd;
          }}
          .button-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
          }}
          .button-container button {{
            font-size: 20px;
            margin: 10px;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            transition: opacity 0.3s;
            color: #fff;
          }}
          .button-container button:hover {{
            opacity: 0.8;
          }}
          .mx-button {{
            background-color: #0088cc;
          }}
          .vlc-button {{
            background-color: #ff8f00;
          }}
          .playit-button {{
            background-color: #d32f2f;
          }}
          .save-button {{
            background-color: #673ab7;
          }}
          .telegram-button {{
            background-color: #009688;
          }}
        </style>
      </head>
      <body>
        <h4>File Name : {file_data.file_name}</h4>
        <h5>Click on 👇 button to watch/download in your favorite player</h5>
        <div class="button-container">
          <button
            class="mx-button"
            onclick="window.location.href = 'intent:{current_url}#Intent;package=com.mxtech.videoplayer.ad;S.title={file_data.file_name};end'"
          >
            WATCH IN MX PLAYER
          </button>
          <button
            class="vlc-button"
            onclick="window.location.href = 'vlc://{current_url}'"
          >
            WATCH IN VLC PLAYER
          </button>
          <button
            class="playit-button"
            onclick="window.location.href = 'playit://playerv2/video?url={current_url}&amp;title={file_data.file_name}'"
          >
            WATCH IN PLAYIT PLAYER
          </button>
          <button
            class="save-button"
            onclick="window.location.href = '{current_url}'"
          >
            DOWNLOAD FILE
          </button>
          <button
            class="telegram-button"
            onclick="window.location.href = 'https://telegram.me/RahulReviewsYT'"
          >
            JOIN ON TELEGRAM
          </button>
        </div>
      </body>
    </html>
    '''

    html += html_code
    return html
