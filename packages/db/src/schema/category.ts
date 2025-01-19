import { relations } from "drizzle-orm";
import { foreignKey, uniqueIndex } from "drizzle-orm/pg-core";

import { pgTable, timestamps } from "./utils";

export const category = pgTable('category', (t) => ({
  id: t.uuid().notNull().primaryKey().defaultRandom(),
  name: t.varchar({ length: 30 }).unique().notNull(),
  parentId: t.uuid(),
  ...timestamps(t),
}),
(category) => [
  uniqueIndex('category_name_idx').on(category.name),
  foreignKey({
    columns: [category.parentId],
    foreignColumns: [category.id],
    name: 'parent',
  })
]);

export const categoryRelations = relations(category, ({ one, many }) => ({
  parent: one(category, {
    fields: [category.parentId],
    references: [category.id],
    relationName: 'parent_to_children_category',
  }),
  children: many(category, { relationName: 'parent_to_children_category' }),
})); 

export default category;