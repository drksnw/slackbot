"""Sample Slack ping bot using asyncio and websockets."""
import asyncio
import json
import signal

import aiohttp

import websockets

from config import DEBUG, TOKEN
from prototype import get_forecast

from slackclient import SlackClient

sc = SlackClient(TOKEN)
print(sc.api_call("api.test"))

def sendMessage(chan, txt):
    global sc
    print("Lol :: "+txt)
    print("I'm sending message to "+chan)
    return sc.api_call("chat.postMessage", token=TOKEN, as_user="true", channel=chan, text=txt)

RUNNING = True


async def producer():
    """Produce a ping message every 10 seconds."""
    await asyncio.sleep(10)
    return json.dumps({"id": 1, "type": "ping"})


async def consumer(message):
    """Consume the message by printing them."""
    print(message)
    dico = json.loads(message)
    if 'type' in dico and dico['type'] == 'message' and 'channel' in dico and 'text' in dico and 'bot_id' not in dico:
        vals = dico['text'].split(' ')
        if len(vals) == 2:
            print(dico['channel'])
            #sc.rtm_send_message(dico['channel'], get_forecast(vals[0], vals[1]))
            print(sendMessage(dico['channel'], get_forecast(vals[0], vals[1])))
        elif dico['text'].startswith(":middle_finger:"):
            #Spreads love.
            for i in range(5):
                sendMessage(dico['channel'], ":heart:")
        elif dico['text'] == "42":
            sendMessage(dico['channel'], "\"Six by nine. Forty two.\"\n\"That's it. That's all there is.\"\n\"I always thought something was fundamentally wrong with the universe\"")
        elif ":heart:" in dico['text']:
            sendMessage(dico['channel'], "You can't love a bot...")
        elif len(vals) > 2:
            sendMessage(dico['channel'], "Wow, I can't handle that much information !! :scream: \n If your city have multiple words in its name, please write it in one word :wink: \n Example: *La Neuveville CH* becomes *LaNeuveville CH*")
        else:
            sendMessage(dico['channel'], "Please send your city followed by the country ! :wink: \nExample: Bern CH\nHave fun ! :full_moon_with_face: :full_moon_with_face:")
    else:
        print("That's not interesting")


async def bot(token):
    """Create a bot that joins Slack."""
    if sc.rtm_connect():
        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop) as client:
            async with client.post("https://slack.com/api/rtm.start",
                                   data={"token": TOKEN}) as response:
                assert 200 == response.status, "Error connecting to RTM."
                rtm = await response.json()

        async with websockets.connect(rtm["url"]) as ws:
            while RUNNING:
                listener_task = asyncio.ensure_future(ws.recv())
                producer_task = asyncio.ensure_future(producer())

                done, pending = await asyncio.wait(
                    [listener_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()

                if listener_task in done:
                    message = listener_task.result()
                    await consumer(message)

                if producer_task in done:
                    message = producer_task.result()
                    await ws.send(message)
    else:
        pass

def stop():
    """Gracefully stop the bot."""
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.set_debug(DEBUG)
    #loop.add_signal_handler(signal.SIGINT, stop)
    loop.run_until_complete(bot(TOKEN))
    loop.close()
