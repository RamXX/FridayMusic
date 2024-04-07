# FridayMusic

This program reads your **Daily Notes** from [Obsidian](https://obsidian.md/) and uses AI to determine the "mood" for the entire week. It then recommends appropriate music according to your preferences and plays it automatically. It also recommends a drink for your listening session, based on the mood (can be disabled). 

Technically, you can  point it to any directory with Markdown files as long as they follow the same format as Obsidian's daily notes. It only reads the files that have been created in the last 7 days. The weekly mood is calculated based on weights, with Friday being the most important, then going backwards in the week.

# DSPy

The program uses the powerful [DSPy](https://github.com/stanfordnlp/dspy) framework for AI generation, due to its simplicity and flexibility. It is setup to use GPT 3.5, but it can be adapted to virtually any language model, local or otherwise, all without ever having to change the prompts.

In its current form, it uses only `dspy.Signature` classes. However, it would be fairly easy and more elegant to convert the entire program into a `dspy.Module` that calls those signature instances as needed in the `forward` function. That will have to be left for the future (PRs are welcome).

This program makes extensive use of the [Typed Predictors](https://dspy-docs.vercel.app/docs/building-blocks/typed_predictors) in order to enforce the Pydantic data types outputs. 

## Configuration
You can configure your preferences primarily in two different files, `config.ini` and `config.py`. Eventually, I'd like to consolidate everything on a single file, but this is the current state.

After the installation, create a `.env` file in the main folder and ensure you have `OPENAI_API_KEY=xxxxxx` with your API key.

## Roon Integration
The program is integrated with [Roon](https://roon.app/en/) for music playback.

In the perfect world, I would have liked to create unique playlists, but the Roon API is limited to basic playback and some browsing functionality. It will not allow the direct creation of playlists. I also tried to do this via my music subscription of choice, [Qobuz](https://www.qobuz.com/us-en/discover), but they also lack a public API (shame).

The playback is a locking function unfortunately, so that means the program will need to run during the playback. However, you can Control-C at any point and then manipulate your queue directly on the Roon client.

## Installation
```
git clone https://github.com/RamXX/FridayMusic && cd FridayMusic
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -U
python fridaymusic
```

For Roon integration, you will need to `git clone https://github.com/pavoni/pyroon` separately, go to the `examples` directory, and run the `discovery.py` file. While you run this file, you need to open your Roon app, go to Settings -> Extensions, and authorize the extension listed. 

This will create two files in the `examples` directory: `my_core_id_file` and `my_token_file`. Copy both files to the `FridayMusic` directory. If you change the names or locations, make sure you also change the settings under the `[Roon]` section in the `setup.ini` file.

## Disclaimer

Needless to say, I built this program for me, and it's tailored to my habit of enjoying 90 minutes of music in my dedicated audio room while enjoying a drink every Friday at 6 PM.

However, I figured I release it as an example on how easy it is to integrate DSPy and AI in general into specific tasks that require deterministic output formats. I hope this is useful to others in some form.