import { relations } from "drizzle-orm";

import { pgTable, timestamps } from "./utils";
import { account } from "./account";
import { conversation } from "./conversation";
import { knowledgeBase } from "./knowledge-base";

export const customer = pgTable("customer", (t) => ({
  id: t.uuid().notNull().primaryKey().defaultRandom(),
  email: t.varchar({ length: 255 }).notNull(),
  emailVerified: t.timestamp({ mode: "date", withTimezone: true }),
  name: t.varchar({ length: 255 }).notNull(),
  image: t.varchar({ length: 255 }),
  metadata: t.jsonb(),
  ...timestamps(t),
}));

export const customerRelations = relations(customer, ({ many }) => ({
  conversations: many(conversation),
  knowledgeBase: many(knowledgeBase),
  accounts: many(account),
})); 

export default customer;