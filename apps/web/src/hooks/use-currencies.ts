import { useEffect, useState } from "react";
import { getCurrencies } from "@/services/currencies/get-currencies";
import type { CurrencyInfo } from "@/types/currency";

export function useCurrencies() {
    const [currencies, setCurrencies] = useState<CurrencyInfo[] | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        getCurrencies().then(setCurrencies).catch(() => setError("Could not load currencies."));
    }, []);

    return { currencies, error };
}