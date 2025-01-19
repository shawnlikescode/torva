import { relations } from "drizzle-orm";
import { primaryKey } from "drizzle-orm/pg-core";

import { pgTable } from "./utils";
import { customer } from "./customer";

export const account = pgTable(
  "account",
  (t) => ({
    userId: t
      .uuid()
      .notNull()
      .references(() => customer.id, { onDelete: "cascade" }),
    type: t
      .varchar({ length: 255 })
      .$type<"email" | "oauth" | "oidc" | "webauthn">()
      .notNull(),
    provider: t.varchar({ length: 255 }).notNull(),
    providerAccountId: t.varchar({ length: 255 }).notNull(),
    refresh_token: t.varchar({ length: 255 }),
    access_token: t.text(),
    expires_at: t.integer(),
    token_type: t.varchar({ length: 255 }),
    scope: t.varchar({ length: 255 }),
    id_token: t.text(),
    session_state: t.varchar({ length: 255 }),
  }),
  (account) => [
    primaryKey({
      columns: [account.provider, account.providerAccountId],
    }),
  ]
);

export const accountRelations = relations(account, ({ one }) => ({
  customer: one(customer, { fields: [account.userId], references: [customer.id] }),
})); 

export default account;