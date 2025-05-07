# RoutineCloud Frontend

This is the frontend part of the RoutineCloud application, built with Vue.js.

## Project Setup

```bash
npm install
```

### Compile and Hot-Reload for Development

```bash
npm run dev
```

### Type-Check, Compile and Minify for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/          # Static assets
├── src/             # Source files
│   ├── assets/      # Static assets for the application
│   ├── components/  # Vue components
│   ├── router/      # Vue Router configuration
│   ├── stores/      # Pinia stores
│   ├── views/       # Vue views
│   ├── App.vue      # Root component
│   └── main.ts      # Entry point
├── .gitignore       # Frontend gitignore
├── package.json     # Frontend dependencies
├── tsconfig.json    # TypeScript configuration
└── vite.config.ts   # Vite configuration
```

## Development

The frontend development server runs on: http://localhost:5173 (default Vite dev server port)

## Notes

This frontend application communicates with the RoutineCloud backend API. Make sure the backend server is running when developing the frontend application.