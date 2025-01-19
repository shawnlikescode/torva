import { relations } from "drizzle-orm";
import { index } from "drizzle-orm/pg-core";

import { pgTable, timestamps } from "./utils";
import { conversation } from "./conversation";

export const message = pgTable("message", (t) => ({
  id: t.uuid().notNull().primaryKey().defaultRandom(),
  conversationId: t.uuid().notNull().references(() => conversation.id, { onDelete: "cascade" }),
  content: t.text().notNull(),
  role: t.varchar({ length: 50 }).$type<"user" | "assistant" | "system">().notNull(),
  ...timestamps(t),
  metadata: t.jsonb(),
}), (message) => [
  index("message_conversation_id_idx").on(message.conversationId),
]);

export const messageRelations = relations(message, ({ one }) => ({
  conversation: one(conversation, { fields: [message.conversationId], references: [conversation.id] }),
})); 

export default message;