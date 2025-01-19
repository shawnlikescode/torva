import { relations } from "drizzle-orm";

import { pgTable, timestamps } from "./utils";
import { conversation } from "./conversation";

export const feedback = pgTable("feedback", (t) => ({
  id: t.uuid().notNull().primaryKey().defaultRandom(),
  conversationId: t.uuid().notNull().references(() => conversation.id, { onDelete: "cascade" }),
  rating: t.integer(),
  comment: t.text(),
  ...timestamps(t),
  helpful: t.boolean(),
}));

export const feedbackRelations = relations(feedback, ({ one }) => ({
  conversation: one(conversation, { fields: [feedback.conversationId], references: [conversation.id] }),
})); 

export default feedback;