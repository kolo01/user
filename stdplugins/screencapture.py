# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events
import os
import requests

ACCESS_KEY = os.environ.get("SCREEN_SHOT_LAYER_ACCESS_KEY")

@borg.on(events.NewMessage(pattern=r".screencapture (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(ACCESS_KEY, input_str), stream=True)
    if "invalid_access_key" not in response_api.text:
        temp_file_name = "screenshotlayer.png"
        with open(temp_file_name, "wb") as fd:
            for chunk in response_api.iter_content(chunk_size=128):
                fd.write(chunk)
        try:
            await borg.send_file(event.chat_id, temp_file_name, caption=input_str, force_document=False)
            await event.delete()
        except:
            await event.edit(response_api.text)
        os.remove(temp_file_name)
    else:
        await event.edit(response_api.text)
