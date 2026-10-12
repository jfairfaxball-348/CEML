# RUN1 conditional chain record — 2026-10-12

The owner explicitly requested agent execution of pilot 1 and supplied the acknowledgement and commands. On its success the owner requested commit, merge and push, authorised the next 1440 integers, specified pilot 3 as the following 14400, and requested a single command to launch the subsequent 100000 integers personally. The owner has now executed that command and shown its `CONDITIONAL_RUN_COMPLETE` output; read-only verification of the saved records confirms all seven additional batches. These pilot widths are an owner-directed exception to the runbook's usual batch-2/doubling schedule; the frozen maximum of 14400 per batch and all identity, budget and verification requirements remain in force.

| Pilot | Half-open interval | Width | Status | Certificate digest |
|---|---|---:|---|---|
| 1 | `[2392518188130438742016,2392518188130438742160)` | 144 | COMMITTED; verification, replay and ledger passed | `99d6907248aa02a517d638469d60ab0f659af0a045b0444531e93fde1380f8a2` |
| 2 | `[2392518188130438742160,2392518188130438743600)` | 1440 | COMMITTED; verification, replay and ledger passed | `cebd2cf5d6e0ae327c3e54a6bc6dfef5e89358bf6a9aecbb2f5220b5431eb77e` |
| 3 | `[2392518188130438743600,2392518188130438758000)` | 14400 | COMMITTED; verification, replay and ledger passed | `ab213f7ba9016bc54afe67873747e605dd88813480a695e8fb54b9b0821f46e6` |

The owner's live continuation consists of these seven committed batches. The launcher reported verification, replay, chain audit and inspection before each extension; the agent subsequently re-audited the complete saved chain and separately verified, replayed and inspected the final batch.

| Batch | Half-open interval | Width | Certificate digest |
|---|---|---:|---|
| 4 | `[2392518188130438758000,2392518188130438772400)` | 14400 | `8a879d23f28934c9b93e4970ef4813a01b00e507ffeeba146bf9be8e5976b83f` |
| 5 | `[2392518188130438772400,2392518188130438786800)` | 14400 | `5e68013a6ac6291b1502442ef2912788ad150fecfe78e4413099c4cab96b0ed3` |
| 6 | `[2392518188130438786800,2392518188130438801200)` | 14400 | `e8fbc86a04897105a4227da3ed8ab560e7a745d9c2a1b44e70ca18cf4fe4ba16` |
| 7 | `[2392518188130438801200,2392518188130438815600)` | 14400 | `d1d7e3a0f27b318efd9f5b69296a143eb43d0f96c71cdb5bbdeab872b3743063` |
| 8 | `[2392518188130438815600,2392518188130438830000)` | 14400 | `e9d4ccb4837bb257a77430dc15361c3ed2205b7beb3a5d2a50701ceabc5d6e20` |
| 9 | `[2392518188130438830000,2392518188130438844400)` | 14400 | `f936d6262777af7933143e7576b8e776c4a936eadc6091f16479005c694868f7` |
| 10 | `[2392518188130438844400,2392518188130438858000)` | 13600 | `5f46665571ef5e85ed629576cd1e7f231ba1c8abe7a7d7975d408d94c14be17a` |

The owner then used the quantity-only command for another 100000 integers. The saved chain was audited and the last batch separately replayed and inspected before recording this additional prefix.

| Batch | Half-open interval | Width | Certificate digest |
|---|---|---:|---|
| 11 | `[2392518188130438858000,2392518188130438872400)` | 14400 | `bf87af5c756ad390d47e9fb33153cce81d29cda1e430ed0bdf895dfac4f65d74` |
| 12 | `[2392518188130438872400,2392518188130438886800)` | 14400 | `57cb4c724b07252d76642b69b9267c7bf3450bd47b88585d50105ca1beaccc27` |
| 13 | `[2392518188130438886800,2392518188130438901200)` | 14400 | `7ba5446572317e0bb372bce29086ac3bff2a7161db40b3f9706dcbc64937424d` |
| 14 | `[2392518188130438901200,2392518188130438915600)` | 14400 | `e6bd0fd0d07f39e244cad25f55f34d776bc08a256407f54eadd916c0c6da8f47` |
| 15 | `[2392518188130438915600,2392518188130438930000)` | 14400 | `8bb0a9f5d5a1da975e27f5792e8d5c1a6331eb3afa85e561e9e0b3dd4bfda712` |
| 16 | `[2392518188130438930000,2392518188130438944400)` | 14400 | `6d6d2cca47253ebadfdf62eb0823f01a142b4fdc956d9880022aded9a84b535a` |
| 17 | `[2392518188130438944400,2392518188130438958000)` | 13600 | `c02b25bf00b1dfd64d9eb7a33f054038c333655043ac495a2e5e2a185137278d` |

The owner's subsequent 1000000-integer continuation added 70 committed batches, 18–87, covering exactly `[2392518188130438958000,2392518188130439958000)`. Full-chain audit and separate final certificate verification, reference replay and checkpoint inspection passed read-only confirmation before publication.

| Batch | Half-open interval | Width | Certificate digest |
|---|---|---:|---|
| 18 | `[2392518188130438958000,2392518188130438972400)` | 14400 | `139fd4519dbebb31343e51ba1791b17fb447ccfd7ccb3f765ce16a7b4b53e4d9` |
| 19 | `[2392518188130438972400,2392518188130438986800)` | 14400 | `4ba4aa2a67cb8aabb8083f306d7050a1c6ba8d65d1f559aaa54c80e6fee525e4` |
| 20 | `[2392518188130438986800,2392518188130439001200)` | 14400 | `5a706073ba22d8545d6d04c83d177c27f59e5a388548d27dd1c83bf009e253a1` |
| 21 | `[2392518188130439001200,2392518188130439015600)` | 14400 | `afeaff6687d96799036a47b4d8a78d092771bac1cc55e0c95a77765a10921c5c` |
| 22 | `[2392518188130439015600,2392518188130439030000)` | 14400 | `a93f388059046038a89e5355976e4d8ac42bf2796bee5b568dbe1f7e69533583` |
| 23 | `[2392518188130439030000,2392518188130439044400)` | 14400 | `b30f7a1fb90ce5b9f81645e2818a86f23d722a0e6f2aa3de17543bb2e873c3ea` |
| 24 | `[2392518188130439044400,2392518188130439058800)` | 14400 | `e5c57527908942c697a12334f67c30dcee886e98790593297b470509bfd5b2e9` |
| 25 | `[2392518188130439058800,2392518188130439073200)` | 14400 | `bdfe1af928a0814b434bc73d09f6388061bad93682705a3f2974f021422b2ddb` |
| 26 | `[2392518188130439073200,2392518188130439087600)` | 14400 | `21a0bae47f655b39a758c4bf7a719696349bf07e97369d58b3d16135d4de71b1` |
| 27 | `[2392518188130439087600,2392518188130439102000)` | 14400 | `efc79346df4be873c65bcf43a75cdc1de5cfa31bab5b8a039e17ee572ed722af` |
| 28 | `[2392518188130439102000,2392518188130439116400)` | 14400 | `d7a449f75d5d8bb2ccf43ea61a4b1250c707cc5fbb43d268f0a8ca4920d5456b` |
| 29 | `[2392518188130439116400,2392518188130439130800)` | 14400 | `47f5aea8eea4eda4c5869ef0ce7c9b38799e3511c7bf379937b89347893321aa` |
| 30 | `[2392518188130439130800,2392518188130439145200)` | 14400 | `4f0906b51b084c541985bbd6c12e953f32c530d2ffffc53465f0b59261efc1b9` |
| 31 | `[2392518188130439145200,2392518188130439159600)` | 14400 | `aec18796d34b0e5602375d2728b9e49de17ed43a63b0ef1f83f2c7baa65c4a93` |
| 32 | `[2392518188130439159600,2392518188130439174000)` | 14400 | `5a0ba4aedee5855aa514358d10a4d4fee2f5f743a405a6f5052d380e38e4a737` |
| 33 | `[2392518188130439174000,2392518188130439188400)` | 14400 | `8f8d87cd347647d83e88570bb4a08370b3c74a0b3b58d5ebad8aeedc44ecb4a9` |
| 34 | `[2392518188130439188400,2392518188130439202800)` | 14400 | `b754f01a37a438b4e80b7ba80a804cb2fa5ed5fc41cf68c08e391d89af24ef45` |
| 35 | `[2392518188130439202800,2392518188130439217200)` | 14400 | `3841cf963bf16ef76189b5fde47297534070118312aa653b39e65dbdb687404c` |
| 36 | `[2392518188130439217200,2392518188130439231600)` | 14400 | `206842d532d55f4ca180a643a9a3c6ed8d25ef9265139ce8cbd0ca1111569758` |
| 37 | `[2392518188130439231600,2392518188130439246000)` | 14400 | `d93878d1b7ef178a8f2db6821d752ad0d39cc37b9622a7e13fd5f99b2b6f0fe6` |
| 38 | `[2392518188130439246000,2392518188130439260400)` | 14400 | `88db39349c7eb7bbbfc8d2f36c1c2afa609160abf050b6038bf8901e45989e4f` |
| 39 | `[2392518188130439260400,2392518188130439274800)` | 14400 | `6c8050aa4f9887e00905b839cdc8b7a727f940934212bed7a794ee6780ee379c` |
| 40 | `[2392518188130439274800,2392518188130439289200)` | 14400 | `e1ee463e541078f64fd3b10dbf21fb0e327b80bb2999862f52413d3a14b2a629` |
| 41 | `[2392518188130439289200,2392518188130439303600)` | 14400 | `4fb0023885aaef605e76c4bbcff375f9dcc81e0cefa6bde286ed495f55e8e14a` |
| 42 | `[2392518188130439303600,2392518188130439318000)` | 14400 | `b2a04af965f1e8bd256a223abf00b6c8d842dd71beda084d8df344529feab272` |
| 43 | `[2392518188130439318000,2392518188130439332400)` | 14400 | `358e1ea3a13a38afec53bb11dbf2df60c0aae36f90784ef163e820d2bbcaeeec` |
| 44 | `[2392518188130439332400,2392518188130439346800)` | 14400 | `8c35d490320e4c4dfde757075bbf5ae280d537aa75956942d38c036bd3d55321` |
| 45 | `[2392518188130439346800,2392518188130439361200)` | 14400 | `62b456fcade7519930bf7730a0bc93a5f9489a9da04a62169f8ef2861dfbc0bf` |
| 46 | `[2392518188130439361200,2392518188130439375600)` | 14400 | `2f1cb39b133ba8941709f72a418a504472c1ba2f73a2cd1ad6731b73378e58ff` |
| 47 | `[2392518188130439375600,2392518188130439390000)` | 14400 | `f4942116e13e771c00e1f52a425750d702ab08f0c1ee4711ba98a8ebc924b9aa` |
| 48 | `[2392518188130439390000,2392518188130439404400)` | 14400 | `abec0d1ab059d4b9c06beb0a3bd2e77f5ae9254c5b6ffce5598bfb5108b12402` |
| 49 | `[2392518188130439404400,2392518188130439418800)` | 14400 | `24605fbeccf136acb561d0f762146db9d861fb08f3a4477bbeb389d10c1ee079` |
| 50 | `[2392518188130439418800,2392518188130439433200)` | 14400 | `41ba8001fb0c00d26edde8a87bd4df14e6b92979b0e7b2a0481631cb927b9af0` |
| 51 | `[2392518188130439433200,2392518188130439447600)` | 14400 | `b48ff69bb33e8cc1ef0d9c5e5438e930fef66b95e7be40316e08be17674ebc69` |
| 52 | `[2392518188130439447600,2392518188130439462000)` | 14400 | `ced279235e74afa734e6e198afc6cd51019580ca558a911aade459c3c22f193d` |
| 53 | `[2392518188130439462000,2392518188130439476400)` | 14400 | `b5bac6dd81730c917a26eb60b2bb729108e66e8e4f9b70bda8ea13fec82f4c14` |
| 54 | `[2392518188130439476400,2392518188130439490800)` | 14400 | `bcda14cb150bbf6ed69bd0bd1c1ca7815458245b0b7b5fed57828cf5db16586e` |
| 55 | `[2392518188130439490800,2392518188130439505200)` | 14400 | `4de510c0db5291f4208eaec8dd53d86744abfc570143fcfe736bfa7a06077d90` |
| 56 | `[2392518188130439505200,2392518188130439519600)` | 14400 | `b0c855244bff3671d50060d3cf74e8441c7056a7d376fee8e099f874de5f73a8` |
| 57 | `[2392518188130439519600,2392518188130439534000)` | 14400 | `9e34acb30c20407322b57a5a8d03572503709cb3c9d071d90ae0992a46303247` |
| 58 | `[2392518188130439534000,2392518188130439548400)` | 14400 | `a5026fe2c634ab6ffbde8fb30463e07c2a6d131c8d9adca6c3f3ae44115a7d8b` |
| 59 | `[2392518188130439548400,2392518188130439562800)` | 14400 | `ddc8c250faef927c75b13ff8e8cd19d7644e7854f0ad645f21ec1dfc18eb2d31` |
| 60 | `[2392518188130439562800,2392518188130439577200)` | 14400 | `89ae89ca08f4889c2107327847bd4278b32fa19c6e80eec6714e282234e57fef` |
| 61 | `[2392518188130439577200,2392518188130439591600)` | 14400 | `5c85332efc4c3d7e828e53d9069187288d18ec4bcdffc697a95046c4047c3d10` |
| 62 | `[2392518188130439591600,2392518188130439606000)` | 14400 | `6222e9ee7316f0a5fd04bb9d4276aca113efd669d24c7ac3eb0943308143dc8d` |
| 63 | `[2392518188130439606000,2392518188130439620400)` | 14400 | `e451da720ab8e0e4ff003cd18ab333177c4d0a9a798fc98d5be262b1e2c6ce82` |
| 64 | `[2392518188130439620400,2392518188130439634800)` | 14400 | `af5d7333b13c34eb4021322a6f22ab150cace99fe6afe13a31384e4314495aeb` |
| 65 | `[2392518188130439634800,2392518188130439649200)` | 14400 | `a0a0ebedf54dfe6cf85c1b620b7654c789cbe6f8d498f5447ffe9218ab3a49f6` |
| 66 | `[2392518188130439649200,2392518188130439663600)` | 14400 | `d17e1e672426d5fbc6d79a6ab3494139e3fd0adc91c3185efb035a3a74963fd0` |
| 67 | `[2392518188130439663600,2392518188130439678000)` | 14400 | `7ee39b73f61a6db17643119bc60c9bdc622eae921fcde1ac18fe3c35f19876f0` |
| 68 | `[2392518188130439678000,2392518188130439692400)` | 14400 | `d063e2ffef2f75960778a60ceaa3223fc9728391b732aa8fc703101bc9733635` |
| 69 | `[2392518188130439692400,2392518188130439706800)` | 14400 | `d9393ed0be9b547298ba04c4d50ecf1b8d66d49c822a3382a1030c5c30211196` |
| 70 | `[2392518188130439706800,2392518188130439721200)` | 14400 | `049f894a914937b872248e56ebf7a7d882a631f009a00b08fb9b41edd93a4f9d` |
| 71 | `[2392518188130439721200,2392518188130439735600)` | 14400 | `a7d317be803d4c61482b624c92d93f5d89e7e4ab7416ee19f0f069b8e41675c6` |
| 72 | `[2392518188130439735600,2392518188130439750000)` | 14400 | `017e91f7e24d727ffab1907503e528591b67b4a4ce132c9a478b54e253fc9a5e` |
| 73 | `[2392518188130439750000,2392518188130439764400)` | 14400 | `529302be8bf0c008e8358d9354626a53ed8ddb73da8af05b8634c46eb199de02` |
| 74 | `[2392518188130439764400,2392518188130439778800)` | 14400 | `e4c8e9aa040916a402dea1a715fbd1c29c0888777a137078a8e1c85338b02dd4` |
| 75 | `[2392518188130439778800,2392518188130439793200)` | 14400 | `256030aaabc808907195672dcdc306af42f7f938126e3a5297af8028a498389f` |
| 76 | `[2392518188130439793200,2392518188130439807600)` | 14400 | `a3ec04827d44a42ac3be554c9be49d9ace0105409e78be551de3ceac22852e1d` |
| 77 | `[2392518188130439807600,2392518188130439822000)` | 14400 | `9b7f67787dbf3459c68ec4e189d8572e3ce29231e38715dfe2287f766ce7bb86` |
| 78 | `[2392518188130439822000,2392518188130439836400)` | 14400 | `7f4ad4395115dbd9933a8dc02f12aec50298fd81d6a88709b3fc3b18ba2e23f1` |
| 79 | `[2392518188130439836400,2392518188130439850800)` | 14400 | `f81f6bbd996d3102a14c7630d45ee4c58ad7fdbfbaf8e6f07316696ed02317ea` |
| 80 | `[2392518188130439850800,2392518188130439865200)` | 14400 | `1bd08a4d2680dcd3c44ffdb340bd8b30c9403d5d35b57a7e75dc8800c4071513` |
| 81 | `[2392518188130439865200,2392518188130439879600)` | 14400 | `2a6af196a8de969710cd6961409efd5e661d11378883bd0e80aa96421b004031` |
| 82 | `[2392518188130439879600,2392518188130439894000)` | 14400 | `eca4d0a63f6fdb7109501770c570b9c13712d7a88f400af94ebd05c568953dad` |
| 83 | `[2392518188130439894000,2392518188130439908400)` | 14400 | `56cc8ce7a26bced06ce90b9a36145d4fd1fe49ea9bbc1367ec89379a71356f45` |
| 84 | `[2392518188130439908400,2392518188130439922800)` | 14400 | `07277b26625338f303e02e1df0fb32694e626ca3f65bdaa49539d9b3bb63c326` |
| 85 | `[2392518188130439922800,2392518188130439937200)` | 14400 | `d3885d023f27e101a06c00f07a2554aa79af81ef4a958cdfc776b81412cc5def` |
| 86 | `[2392518188130439937200,2392518188130439951600)` | 14400 | `69c4ed5062956fe7dfdd8196a77e05f9128efb4b061dcffcc26ec6ff749cf180` |
| 87 | `[2392518188130439951600,2392518188130439958000)` | 6400 | `6f886ebbe57bbc26573560146e5bd73f5ee6f682931a6ab39e67a1a731c4b4bc` |

```text
CEML-FRONTIER-2 conditional batch chain
Run identifier: RUN1-operational-0001
Base kind and tier: operational (author-reported, not replicated)
Assumed, not verified by CEML: every positive integer below B = 2392518188130438742016 converges
  Source and its date: author's project homepage https://pcbarina.fit.vut.cz/, generated 2026-10-11T11:29:26Z
  CEML observation time (UTC): 2026-10-11T12:38:06Z
Verified conditional on that assumption: every integer in [2392518188130438742016,2392518188130439958000) converges
Batches: 87 (1215984 integers)
Genesis digest: a416bf0f89ebdb16911baf830b6c375d280829bd58587dd7787e36f5d3c53caf
Latest certificate digest: 6f886ebbe57bbc26573560146e5bd73f5ee6f682931a6ab39e67a1a731c4b4bc
Snapshot digest: 538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729
Native build digest: c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032
Source commit of pilot 1: 641e7b64acd01397f360a14eb1659107e7732459
Source commit of owner's 100000-integer continuation: 789dca672cdd3bbe9ed7d30d93f465f2e2e47c7b
Source commit at confirmation of batches 11–17: c10da89922e5185d4d0bb8076136a5f991fadd96 (records bind the build digest, not a Git SHA)
Source commit at confirmation of batches 18–87: 8467367a088f9af5a686fd99149320f228fa2d23 (records bind the build digest, not a Git SHA)
Rule counts (E2, Q4, P3, M9, S2K4-03, EXPLICIT): 607992, 303996, 101332, 33777, 42221, 126666
Unresolved: 0
Explicit shortened-map steps computed: 1509975 (923196 odd; 2433171 standard-map steps)
Run dates (UTC): 2026-10-12; certificate filesystem timestamps from 08:53:51Z (pilot 1) to 13:19:16Z (batch 87)
Independent full replay performed: yes, built-in second pass (same author and machine)
Independent reproduction by other code: none
Overlap with externally reported work: expected; not checked against the external project's current state
This is a finite, conditional computational result. It is not a proof of the Collatz conjecture, not a
reproduction of the base, and not a claim of a world-first or of global frontier extension.
```

Pilot 1's native scan and per-frame check took 0.091117 seconds; its whole pilot command took about 2.73 seconds. Checkpoint inspection found generation 1 recoverable, no pending start, no warnings and no temporary files. OS firewall isolation was not applied to this scientific pilot; the runner uses no network. `COMMITTED` denotes an immutable verified local certificate, distinct from a Git commit.

Pilot 2's native scan and per-frame check took 0.145763 seconds; its whole pilot command took about 3.17 seconds. It recomputed 150 explicit starts in 1793 shortened-map steps, with 1095 odd steps (2888 standard-map steps), and resolved all 1440 starts. Its source checkout was local commit `b556cab` with the original accepted build identity. All three verification commands passed; checkpoint inspection again found no pending work or warnings. Its digest was published before pilot 3 and used as that pilot's continuation anchor.

Pilot 3's native scan and per-frame check took 0.716840 seconds; its whole pilot command took about 4.49 seconds. It recomputed 1500 explicit starts in 17759 shortened-map steps, with 10854 odd steps (28613 standard-map steps), and resolved all 14400 starts. Its source checkout was local commit `2ea90ba1d99baf467f9aba65e73a9e2cb98b1842`, with the original accepted build identity. All three verification commands passed; checkpoint inspection found no pending work or warnings. Its digest was the externally published anchor for the owner's live run.

The owner executed the [one-command continuation](RUN1_ONE_COMMAND.md), adding exactly 100000 integers in seven sequential batches within the unchanged 14400 maximum. Those batches computed 123934 explicit shortened-map steps, including 75768 odd steps (199702 standard-map steps). Their certificate filesystem timestamps run from 09:46:42Z to 09:48:32Z; these timestamps are not an exact end-to-end timing measurement. The owner's screenshot showed the final `CONDITIONAL_RUN_COMPLETE` status, and its latest digest and endpoint match the saved ledger. The accepted build still verifies with the original identity. The agent executed no scientific batch in this confirmation session; only read-only verification and aggregate documentation were performed. No further continuation is authorised or started by this record.

The owner's second 100000-integer continuation added `[2392518188130438858000,2392518188130438958000)` in batches 11–17. It computed 124709 explicit shortened-map steps, with 76264 odd steps (200973 standard-map steps). Certificate filesystem timestamps run from 11:01:07Z to 11:03:59Z; these are not an exact whole-command timing measurement. The full ledger, final reference replay and checkpoint inspection passed read-only confirmation. There is no pending work, checkpoint warning or unresolved start. The local continuation receipt matches the 17-batch ledger exactly, and the accepted build identity remains unchanged. No scientific batch was executed by the agent during confirmation or publication.

The owner's 1000000-integer continuation computed 1241380 explicit shortened-map steps, with 758966 odd steps (2000346 standard-map steps). It resolved 104167 explicit starts and all 1000000 total starts, with zero unresolved. The retained local receipt exactly matches the 87-batch ledger and the owner's final printed endpoint, genesis and certificate digest. Final inspection found generation 1 recoverable, no pending start, warnings or temporary files. The accepted build identity is unchanged. The agent ran only read-only checks and publication tools during confirmation, with no new scientific batch.

Saved filesystem timestamps span 11:24:15Z (batch 18 run preparation) to 13:19:16Z (batch 87 certificate), approximately 1 hour 55 minutes 1 second, or 145 integers per second including inter-batch verification. In Europe/London this is 12:24:15–14:19:16 on 2026-10-12. This is an observed file-timestamp span, not an exact end-to-end command timer: initial checks precede preparation and final verification, ledger audit and receipt writing follow the last certificate. No complete elapsed time was retained.

Logging has two separate parts: the offline runner automatically saves local manifests, authority records, checkpoints, immutable certificates and its continuation receipt. An agent or the separate owner-invoked `tools/publication/publish.py` updates and publishes this aggregate Git record only after verification. The runner never commits, pushes or depends on GitHub. Raw batch records, checkpoints and per-integer data remain ignored local files; GitHub carries intervals, aggregate counts, verification statements and digests. This document's published prefix is an external anchor and can lag subsequent local runs until the next verified publication. The optional `tools/publication/live.py` observer uploads provisional informational status to a different branch and never changes this verified aggregate.

The owner removed the separate-device backup requirement; no backup action is outstanding. The reusable PowerShell command is `python C:\CEML\tools\operator\run_frontier.py X`, changing only X. The launcher audits and discovers the latest committed end, checks published/local anchors, reuses this chain's accepted assumption, and saves a local continuation receipt after verification. See `RUN1_ONE_COMMAND.md`. Publication preserves the frozen verifier's identity and every existing batch record.
