import type { TRPCRouterRecord } from "@trpc/server";
import { z } from "zod";

import { desc, eq } from "@torva/db";
import { customer } from "@torva/db/schema";

import { protectedProcedure, publicProcedure } from "../trpc";

export const customerRouter = {
  all: publicProcedure.query(({ ctx }) => {
    return ctx.db.query.customer.findMany({
      orderBy: desc(customer.id),
      limit: 10,
    });
  }),

  byId: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(({ ctx, input }) => {
      return ctx.db.query.customer.findFirst({
        where: eq(customer.id, input.id),
      });
    }),

  delete: protectedProcedure.input(z.string()).mutation(({ ctx, input }) => {
    return ctx.db.delete(customer).where(eq(customer.id, input));
  }),
} satisfies TRPCRouterRecord;
