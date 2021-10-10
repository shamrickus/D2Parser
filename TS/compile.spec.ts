import {doesNotThrow, fail, ok, strictEqual} from 'assert'
import {exec} from 'child_process'
import {Observable} from "rxjs";
import * as fs from "fs";
import * as ts from "typescript";

function runExec(cmd: string): Observable<string> {
    return new Observable<string>(sub => {
        exec(cmd, (error, stdout, stderr) => {
            if (error){
                sub.error(`error: ${error.message}`);
            }
            if (stderr){
                sub.error(`stderr: ${stderr}`);
            }

            sub.next(`stdout: ${stdout}`);
            sub.complete();
        });
    });
}

describe("D2Parser Tests", () => {
    before("setup", () => {
        if(fs.existsSync("../Generated")){
            fs.rmSync("../Generated", {recursive: true});
        }
    });

    it("run for GoN", async () => {
        await runExec("cd .. && python main.py gon latest").toPromise().then(async (next: string | undefined) => {
            strictEqual(fs.existsSync("../Generated/gon/latest/runewords.ts"), true);
            strictEqual(false, ts.createProgram(["../Generated/gon/latest/runewordss.ts"], {}).emit().emitSkipped);
        }).catch((error: string) => {
            fail(error);
        });
    });

    it("run for D2Lod", async () => {
        await runExec("cd .. && python main.py d2lod 114").toPromise().then(async (next: string | undefined) => {
            strictEqual(fs.existsSync("../Generated/d2lod/114/runewords.ts"), true);
            strictEqual(false, ts.createProgram(["../Generated/d2lod/114/runewords.ts"], {}).emit().emitSkipped);
        }).catch((error: string) => {
            fail(error);
        });
    });
});
