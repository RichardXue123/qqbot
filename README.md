# QQBOT

## TODO

1. **Determine Project Structure**
   - Define the overall architecture and organization of the project.
      - Some folders should be accessible to all plugins, e.g. `data/`, `utils/`, `models/`, etc.
   - Current structure:
     ```
      .
      │  bot.py
      └─src
         └─plugins
            │  some_plugin1.py
            │
            └─some_plugin2.py
                     config.py
                     __init__.py
     ```

2. **Establish Plugin Template**
   - Create a standard template for plugins to ensure consistency and ease of development.
   

3. **Generate Unit Test Pipeline for plugins**
   - Establish a unit test pipeline, including document and testing scripts for plugins.
   - See [NoneBug](https://nonebot.dev/docs/best-practice/testing/)

4. **Refactor WebUI Plugin**
   - Refactor the WebUI plugin to improve its functionality and integrate it with the project's standards.

5. **Set Up GitHub Actions**
   - Configure continuous integration and deployment workflows using GitHub Actions.

## Documentation

[Nonebot Docs](https://nonebot.dev/)
[NapCatQQ Docs](https://napneko.github.io/zh-CN/)
[My Webui Project Link](https://github.com/RichardXue123/stable-diffusion-webui)
