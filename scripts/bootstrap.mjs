// Подготовка локального окружения: создаёт .env из .env.example и при первом запуске
// разворачивает локальную базу SQLite с демо-данными. Делает запуск проекта
// командой `npm run dev` самодостаточным (после `npm install`).
//
// Использование:
//   node scripts/bootstrap.mjs            — .env + база (если её нет)
//   node scripts/bootstrap.mjs --env-only — только .env

import { existsSync, copyFileSync } from "node:fs";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const envOnly = process.argv.includes("--env-only");

// 1. .env из .env.example
const envPath = join(root, ".env");
const examplePath = join(root, ".env.example");
if (!existsSync(envPath) && existsSync(examplePath)) {
  copyFileSync(examplePath, envPath);
  console.log("✓ Создан файл .env из .env.example");
}

if (envOnly) process.exit(0);

// 2. База данных (создаём и наполняем только если её ещё нет — правки в админке сохраняются)
const dbPath = join(root, "prisma", "dev.db");
if (!existsSync(dbPath)) {
  console.log("• Локальная база не найдена — создаём и наполняем демо-новостями…");
  try {
    execSync("npx prisma db push --skip-generate", { stdio: "inherit", cwd: root });
    execSync("npx tsx prisma/seed.ts", { stdio: "inherit", cwd: root });
    console.log("✓ База данных готова");
  } catch {
    console.error("⚠ Не удалось подготовить базу автоматически. Запустите: npm run setup");
    process.exit(1);
  }
}
