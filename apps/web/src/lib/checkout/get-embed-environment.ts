/** The embedded checkout needs to be told when it runs in the sandbox. */
export function getEmbedEnvironment(environment: string): "sandbox" | undefined {
    return environment === "sandbox" ? "sandbox" : undefined;
}