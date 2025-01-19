import baseConfig, { restrictEnvAccess } from "@torva/eslint-config/base";
import nextjsConfig from "@torva/eslint-config/nextjs";
import reactConfig from "@torva/eslint-config/react";

/** @type {import('typescript-eslint').Config} */
export default [
  {
    ignores: [".next/**"],
  },
  ...baseConfig,
  ...reactConfig,
  ...nextjsConfig,
  ...restrictEnvAccess,
];
