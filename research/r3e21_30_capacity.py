#!/usr/bin/env python3
"""R3E21-30 planning-only scenario model. No devices/network/science."""
import argparse
import json
import math

B = 2392518188130438742016  # externally author-reported, not reproduced
E = 3000000000000000000000  # exclusive
U = 1 << 40
Q, R = divmod(E - B, U)
N = Q + 1
F = Q + R / U


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--passes", type=int, default=2, choices=[1, 2, 3])
    p.add_argument("--pass-warm-seconds", default="5")
    p.add_argument("--pass-cold-seconds", default="6")
    p.add_argument("--pass-p95-seconds", default="8")
    p.add_argument("--pass-usd-per-hour", default=".89")
    p.add_argument("--workers", type=int, default=1000)
    p.add_argument("--duty", type=float, default=.5)
    p.add_argument("--utilisation", type=float, default=.9)
    p.add_argument("--retry", type=float, default=0)
    p.add_argument("--batch-units", type=int, default=1000)
    p.add_argument("--exception-fraction", type=float, default=0)
    p.add_argument("--cpu-hours-per-exception", type=float, default=0)
    p.add_argument("--disagreement-fraction", type=float, default=0)
    p.add_argument("--arb-hours-per-disagreement", type=float, default=0)
    p.add_argument("--cpu-workers", type=int, default=1000)
    p.add_argument("--cpu-duty", type=float, default=.5)
    p.add_argument("--cpu-utilisation", type=float, default=.9)
    p.add_argument("--cpu-usd-per-hour", type=float, default=0)
    p.add_argument("--record-bytes", type=int, default=1024)
    p.add_argument("--transfer-bytes", type=int, default=1024)
    p.add_argument("--storage-months", type=float, default=1)
    p.add_argument("--storage-usd-per-gb-month", type=float, default=.07)
    p.add_argument("--egress-usd-per-gb", type=float, default=0)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    def values(x):
        v = [float(t) for t in x.split(",")]
        # A single number applies to each pass; explicit per-source list otherwise.
        return v * a.passes if len(v) == 1 else v

    warm, cold = values(a.pass_warm_seconds), values(a.pass_cold_seconds)
    p95, price = values(a.pass_p95_seconds), values(a.pass_usd_per_hour)
    assert all(len(v) == a.passes for v in [warm, cold, p95, price])
    assert all(w > 0 and c >= w and pp >= w and pr >= 0
               for w, c, pp, pr in zip(warm, cold, p95, price))
    assert a.workers > 0 and a.cpu_workers > 0 and a.batch_units > 0
    assert 0 < a.duty <= 1 and 0 < a.utilisation <= 1
    assert 0 < a.cpu_duty <= 1 and 0 < a.cpu_utilisation <= 1
    assert 0 <= a.retry < 1
    assert 0 <= a.exception_fraction <= 1 and 0 <= a.disagreement_fraction <= 1
    for v in (a.cpu_hours_per_exception, a.arb_hours_per_disagreement,
              a.cpu_usd_per_hour, a.record_bytes, a.transfer_bytes,
              a.storage_months, a.storage_usd_per_gb_month, a.egress_usd_per_gb):
        assert v >= 0
    launches = math.ceil(N / a.batch_units)
    sources = []
    for i in range(a.passes):
        hours = (F * warm[i] * (1 + a.retry) +
                 launches * (cold[i] - warm[i])) / 3600
        sources.append(dict(source=i + 1, warm_p50_seconds=warm[i],
                            cold_p50_seconds=cold[i], warm_p95_seconds=p95[i],
                            gpu_hours=hours, cost_usd=hours * price[i]))
    gpu_hours = sum(s["gpu_hours"] for s in sources)
    gpu_cost = sum(s["cost_usd"] for s in sources)
    cpu_hours = N * (a.exception_fraction * a.cpu_hours_per_exception +
                     a.disagreement_fraction * a.arb_hours_per_disagreement)
    gpu_days = gpu_hours / (24 * a.workers * a.duty * a.utilisation)
    cpu_days = cpu_hours / (24 * a.cpu_workers * a.cpu_duty * a.cpu_utilisation)
    receipts = N * a.passes * (1 + a.retry)
    ledger_gb = receipts * a.record_bytes / 1e9
    traffic_gb = receipts * a.transfer_bytes / 1e9
    other_cost = (cpu_hours * a.cpu_usd_per_hour +
                  ledger_gb * a.storage_months * a.storage_usd_per_gb_month +
                  traffic_gb * a.egress_usd_per_gb)
    out = dict(full_units=Q, partial_starts=R, unit_ids=N,
               equivalent_full_width_units=F, per_source=sources,
               gpu_hours=gpu_hours, cpu_hours=cpu_hours,
               gpu_calendar_days=gpu_days, cpu_calendar_days=cpu_days,
               calendar_critical_path_days=max(gpu_days, cpu_days),
               expected_receipts=receipts, ledger_decimal_gb=ledger_gb,
               transfer_decimal_gb=traffic_gb, gpu_cost_usd=gpu_cost,
               total_modeled_cost_usd=gpu_cost + other_cost,
               fleet_p95="UNKNOWN: empirical per-unit p95 is not fleet p95")
    if a.self_test:
        assert Q == 552501489 and R == 350507499520 and N == 552501490
        assert Q * U + R == E - B
        assert abs(F - 552501489.3187847) < 1e-5
        assert len(sources) == a.passes
        assert out["calendar_critical_path_days"] >= gpu_days
        assert out["calendar_critical_path_days"] >= cpu_days
        print("R30_MODEL_SELF_TEST_PASS")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
