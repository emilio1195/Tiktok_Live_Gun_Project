from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent
import gpiozero, time
#import os
#from dotenv import load_dotenv, dotenv_values
#load_dotenv()

#########Init Ports###########
led = gpiozero.LED(18)
##################


##########Methods #############
def shoothing(times_r):
    for n in range(1, times_r):
        led.on()
        time.sleep(0.5)
        led.off()
#############################

#tiktok_id = os.getenv("tiktok_uniq_id")
tiktok_id="@soyninja50"

#Create the client
client: TikTokLiveClient = TikTokLiveClient(unique_id=tiktok_id)

#Listen to an event with decorator
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

#Or, add it manually via "client,add_listener()"
async def on_comment(event: CommentEvent) -> None:
    print(f"{event.user.nickname} -> {event.comment}")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    client.logger.info("Received a gift!")

    # Can have a streak and streak is over
    if event.gift.streakable and not event.streaking:
        print(f"{event.user.unique_id} ({event.user.nickname}) sent {event.repeat_count}x \"{event.gift.name}\"")
        print(f"  Gift Diamonds: {event.gift.diamond_count}")
        print(f"  Gift Infor: {event.gift}")
        #shoot
        shoothing(event.repeat_count)

    # Cannot have a streak
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.name}\"")
        shoothing(event.repeat_count) 
#client.add_listener(CommentEvent, on_comment)

if __name__ == '__main__':
    #Run the client and block main thread
    # Enable debug info
    #client.logger.setLevel(LogLevel.INFO.value)
    #await client.start() to run non-blocking
    client.run()