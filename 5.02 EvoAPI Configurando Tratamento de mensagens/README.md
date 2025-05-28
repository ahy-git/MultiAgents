videoMessage:

ideo Message API Structure
The structure of a video message in the Evolution API includes several key components that define the message's content and metadata. Here is a breakdown of the structure based on the available context:

Key: Identifies the message in the chat.
remoteJid: The recipient's JID (Jabber ID).
fromMe: Indicates whether the message was sent by the user.
id: The unique ID of the message.
participant: The participant in the chat to whom the message was sent.
Message: Contains the actual content of the message.
videoMessage: Details of the video message.
url: The URL of the video.
mimetype: The MIME type of the video.
caption: The caption text of the video.
fileSha256: The SHA-256 hash of the video file.
fileLength: The length of the video file.
height: The height of the video.
width: The width of the video.
mediaKey: The media key of the video.
fileEncSha256: The SHA-256 hash of the encrypted video file.
directPath: The direct path to the video.
mediaKeyTimestamp: The timestamp of the media key.
jpegThumbnail: The JPEG thumbnail of the video.
contextInfo: Additional context information.
messageTimestamp: The timestamp of the message, represented as a string.
status: The status of the message, such as sent, received, or pending.
This structure is similar to the structure of other message types, such as text and image messages, but with specific fields tailored to video content. For example, the videoMessage field includes details like the video's URL, MIME type, and dimensions, which are not present in text or image messages. 