# Melius Operarius Engine

Melius Operarius is an AI-driven website management engine that operates based on instructions stored in a [Pantry](https://getpantry.cloud/) bucket. It functions as a virtual programmer that can update themes, create pages, and manage dynamic components.

## 🚀 Key Features

- **Pantry Integration**: All instructions are fetched from a remote Pantry bucket.
- **Theme Management**: AI can update website colors and themes based on descriptions or specific hex codes.
- **Dynamic Pages**: Create new pages with improved content formatting (e.g., 2-column layouts for comparisons).
- **Strict Text**: Support for text that must remain unchanged by the AI.
- **Special Tags**:
  - `{form}`: Automatically creates a Pantry bucket for submissions and connects it to the website.
  - `{countdown}`: Adds a functional countdown timer.
  - `{live_time}`: Displays the current time.
  - `{sales_banner}` / `{discount_banner}`: Festive or promotional banners.
  - `{product_banner}`: Showcases products with images and purchase info.
  - `{image}` / `{video}`: Embeds media directly.
- **Holiday Awareness**: Automatically adds New Year wishes or offers if detected.

## 🛠️ Setup

1. **Pantry ID**: Get your Pantry ID from [getpantry.cloud](https://getpantry.cloud/).
2. **Environment Variables**:
   - `PANTRY_ID`: Your Pantry ID.
   - `OPENROUTER_API_KEY_1`: Your primary API key for OpenRouter.
3. **Pantry Structure**: Initialize a basket named `melius_instructions` and one with 'melius_forms' with the structure defined in `PANTRY_STRUCTURE.md`.
4. **How to use**: Log in with you pantry id in [https://melius-operarius-control.vercel.app] to get started.

## 📂 Project Structure

- `melius-engine/`: Core logic (Python).
  - `operarius.py`: The main engine logic handling Pantry and AI operations.
  - `agent.py`: Orchestrator.
- `PANTRY_STRUCTURE.md`: Detailed JSON schema for your Pantry instructions.
- `test-website/`: A sample website for testing the engine's capabilities.

## 🔄 How it Works

1. The engine fetches instructions from the `melius_instructions` basket.
2. It scans the repository files.
3. The AI plans modifications based on the instructions and current date (for holidays).
4. If a `{form}` tag is used, the AI:
   - Creates a new Pantry bucket for that form.
   - Registers it in the `melius_forms` basket.
   - Injects JavaScript into the website to handle submissions.
5. Changes are applied to the UI-related files.
