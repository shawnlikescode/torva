import { relations } from "drizzle-orm";

import { pgTable } from "./utils";
import { customer } from "./customer";

export const session = pgTable("session", (t) => ({
  sessionToken: t.varchar({ length: 255 }).notNull().primaryKey(),
  userId: t
    .uuid()
    .notNull()
    .references(() => customer.id, { onDelete: "cascade" }),
  expires: t.timestamp({ mode: "date", withTimezone: true }).notNull(),
}));

export const sessionRelations = relations(session, ({ one }) => ({
  customer: one(customer, { fields: [session.userId], references: [customer.id] }),
})); 

export default session;