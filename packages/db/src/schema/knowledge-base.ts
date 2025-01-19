import { relations } from "drizzle-orm";
import { index } from "drizzle-orm/pg-core";

import { pgTable, timestamps } from "./utils";
import { category } from "./category";
import { customer } from "./customer";

export const knowledgeBase = pgTable("knowledge_base",
  (t) => ({
    id: t.uuid().notNull().primaryKey().defaultRandom(),
    customerId: t.uuid().notNull().references(() => customer.id, { onDelete: "cascade" }),
    title: t.varchar({ length: 255 }).notNull(),
    content: t.text().notNull(),
    categoryId: t.uuid().references(() => category.id),
    status: t.varchar({ length: 50 }).$type<"draft" | "published" | "archived">().notNull().default("draft"),
    ...timestamps(t),
    metadata: t.jsonb(),
  }),
  (knowledgeBase) => [  
    index("knowledge_base_customer_id_idx").on(knowledgeBase.customerId),
  ]
);

export const knowledgeBaseRelations = relations(knowledgeBase, ({ one }) => ({
  category: one(category, { fields: [knowledgeBase.categoryId], references: [category.id] }),
  customer: one(customer, { fields: [knowledgeBase.customerId], references: [customer.id] }),
})); 

export default knowledgeBase;