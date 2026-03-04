# Интеграция roboto_origin с OpenClaw

Связка железной платформы (roboto_origin) и платформы AI-агентов (OpenClaw) для zero-code управления роботом.

---

## Цель

AI-агенты OpenClaw сами генерируют/пишут систему управления роботом по команде на естественном языке. Примеры: «подними руку», «подойди к стулу», «возьми красный кубик и положи в коробку».

---

## Архитектура

```
Пользователь (Telegram/WhatsApp/веб)
    ↓
OpenClaw Gateway
    ↓
AI Agent (Pi / Claude Code / Gemini / Qwen VLM)
    ↓
Генерация кода или параметров движения
    ↓
atom01_deploy (ROS2 + железо)
    ↓
Робот Atom01 (roboto_origin)
```

---

## OpenClaw Robotics

[OpenClaw Robotics Community](https://www.openclawrobotics.com/) адаптирует OpenClaw под робототехнику:

- **ClawBody (Tom Rikert):** мост OpenClaw ↔ физическое железо. MuJoCo для симуляции. Подключен к Reachy Mini.
- **Zero-code robotics:** команда на языке → агент генерирует поведение без ручного кода.
- **Vision-language:** Qwen VLM + Intel RealSense для 3D-восприятия и команд вида «возьми то, что слева».

---

## Work packages

| WP | Задача | Объём |
|----|--------|-------|
| WP-O1 | Развёртывание OpenClaw (self-hosted) | Node 22+, Gateway, onboard |
| WP-O2 | Изучение ClawBody, адаптация под atom01/roboto_origin | Мост OpenClaw → ROS2 / atom01_deploy |
| WP-O3 | Skill «управление роботом» для OpenClaw | API roboto_origin, вызовы из агента |
| WP-O4 | Интеграция vision-language модели | Для команд с визуальным контекстом |
| WP-O5 | Симуляция MuJoCo/Isaac Lab | Безопасная отладка до выкладки на железо |
| WP-O6 | Канал: Telegram/WhatsApp/веб | Управление с телефона |

---

## Синергия с презентацией

Тезис презентации: *«LLM-агент для переноса человеческого языка ТЗ в алгоритм движения робота»*.

- **roboto_origin** — платформа для исполнения (железо, ROS2, deploy)
- **OpenClaw** — реализация концепции LLM-агента
