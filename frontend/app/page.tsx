import { redirect } from "next/navigation";

export default function Home() {
  redirect("/dashboard")
  return (
    <main className="flex min-h-screen items-center justify-center">
      <h1 className="text-2xl font-semibold">Trade Terminal</h1>
    </main>
  );
}
