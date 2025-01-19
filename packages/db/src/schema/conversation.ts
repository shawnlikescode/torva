import { relations } from "drizzle-orm";

import { pgTable, timestamps } from "./utils";
import { customer } from "./customer";
import { message } from "./message";

export const conversation = pgTable("conversation", (t) => ({
  id: t.uuid().notNull().primaryKey().defaultRandom(),
  customerId: t.uuid().references(() => customer.id, { onDelete: "cascade" }),
  status: t.varchar({ length: 50 }).$type<"active" | "resolved" | "pending">().notNull().default("active"),
  subject: t.varchar({ length: 255 }),
  ...timestamps(t),
  resolvedAt: t.timestamp(),
}));

export const conversationRelations = relations(conversation, ({ one, many }) => ({
  customer: one(customer, { fields: [conversation.customerId], references: [customer.id] }),
  messages: many(message),
})); 

export default conversation;