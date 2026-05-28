import type { ContactInput } from "@/lib/validation/contact";

/**
 * Service layer: business logic for handling a contact lead.
 * Decoupled from the HTTP layer (route handler) and from the
 * delivery mechanism (provider) so it can be tested and swapped.
 *
 * In production, implement a provider that sends email (Resend/SMTP)
 * or pushes to a CRM (Bitrix24/amoCRM). The default provider logs.
 */

export type Lead = Omit<ContactInput, "company" | "consent"> & {
  id: string;
  createdAt: string;
  source: string;
};

export interface LeadProvider {
  deliver(lead: Lead): Promise<void>;
}

class ConsoleLeadProvider implements LeadProvider {
  async deliver(lead: Lead): Promise<void> {
    // Replace with real delivery (email/CRM) in production.
    console.info("[lead] received", {
      id: lead.id,
      name: lead.name,
      phone: lead.phone,
      topic: lead.topic || "—",
      source: lead.source,
    });
  }
}

const provider: LeadProvider = new ConsoleLeadProvider();

export async function submitLead(
  input: ContactInput,
  source = "website",
): Promise<Lead> {
  const lead: Lead = {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    source,
    name: input.name,
    phone: input.phone,
    email: input.email || "",
    topic: input.topic || "",
    message: input.message || "",
  };

  await provider.deliver(lead);
  return lead;
}
