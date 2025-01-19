import { sql } from "drizzle-orm";
import { pgTableCreator } from "drizzle-orm/pg-core";
import type { PgColumnsBuilders } from "drizzle-orm/pg-core/columns/all";

export const pgTable = pgTableCreator((name) => `torva_${name}`);

export const timestamps = (t: PgColumnsBuilders) => ({
  createdAt: t.timestamp().defaultNow().notNull(),
  updatedAt: t.timestamp().$onUpdateFn(() => sql`now()`),
}); 