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
        await runExec("cd .. && python main.py gon").toPromise().then(async (next: string | undefined) => {
            strictEqual(fs.existsSync("../Generated/runes.ts"), true);
            strictEqual(false, ts.createProgram(["../Generated/runes.ts"], {}).emit().emitSkipped);
        }).catch((error: string) => {
            fail(error);
        });
    });

    it("run for D2Lod", async () => {
        await runExec("cd .. && python main.py d2lod").toPromise().then(async (next: string | undefined) => {
            strictEqual(fs.existsSync("../Generated/runes.ts"), true);
            strictEqual(false, ts.createProgram(["../Generated/runes.ts"], {}).emit().emitSkipped);
        }).catch((error: string) => {
            fail(error);
        });
    });
});
