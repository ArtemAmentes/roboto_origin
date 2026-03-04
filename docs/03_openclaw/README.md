# OpenClaw

**Платформа AI-агентов для управления роботом на естественном языке.**

---

## Что такое OpenClaw

| Параметр | Значение |
|----------|----------|
| Сайт | [openclaw.ai](https://openclaw.ai/) |
| Лицензия | MIT |
| Развёртывание | Self-hosted |
| Каналы | Telegram, WhatsApp, Discord, веб |

**Ключевые возможности:**
- Агенты с tool use, sessions, memory
- Подключение из кармана через мессенджеры
- Данные на вашем сервере

---

## OpenClaw для робототехники

[OpenClaw Robotics](https://www.openclawrobotics.com/) — сообщество адаптирует платформу под embodied AI:

| Компонент | Назначение |
|-----------|------------|
| **Zero-code robotics** | «Возьми красный кубик» — без написания кода |
| **ClawBody** | Мост к физическому железу, MuJoCo-симуляция |
| **Vision-language** | Gemini Robotics-ER, Qwen VLM |
| **Depth** | Intel RealSense + Qwen VLM для 3D-восприятия |

---

## Содержание раздела

| Документ | Описание |
|----------|----------|
| [Стратегия интеграции OpenClaw](стратегия_интеграции_openclaw.md) | Использование OpenClaw для кода управления |
| [Установка и настройка](установка_и_настройка.md) | Self-hosted deployment |
| [ClawBody и адаптация](clawbody_и_адаптация.md) | Мост OpenClaw → atom01 |
| [Skill «управление роботом»](skill_управление_роботом.md) | API для агентов |

---

## Связанные разделы

- [roboto_origin](../02_roboto_origin/README.md) — платформа исполнения
- [Интеграция OpenClaw + roboto_origin](../02_roboto_origin/интеграция_openclaw.md) — архитектура связки
