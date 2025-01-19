import { authRouter } from "./router/auth";
import { customerRouter } from "./router/customer";
import { createTRPCRouter } from "./trpc";

export const appRouter = createTRPCRouter({
  auth: authRouter,
  customer: customerRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;
