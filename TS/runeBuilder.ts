import {IMultiProperty, MultiProperty,,  Rune, SocketSlotType} from "../../pages/armory/armory.service";
import {runes as runesLevels} from "./runesLevels";
import {runes} from "./runes";

function ConstructRunes() {
    let constructed = <Rune[]>[];
    for(let rune in runes) {
        constructed.push(RuneBuilder(runes[rune]));
    }
    return constructed;
}

function RuneBuilder(rune: any) : Rune {
    let parsedRune = new Rune();
    parsedRune.Name = rune["letter"];
    parsedRune.Id = rune["code"];
    parsedRune.Level = runesLevels.find(value => value["Id"] == parsedRune.Id)["Level"];
    parsedRune.Properties = MultiPropetyBuilder(rune["Properties"]);
    return parsedRune;
}
function MultiPropetyBuilder(properties: any[]): IMultiProperty[]{
    let props = <IMultiProperty[]>[];
    for(let type in properties) {
        let slot = new SocketSlotType(properties[type]);
        let slotName = slot.SlotTypeToString();
        for (let i in properties[type][slotName]) {
            let property = properties[type][slotName][i];
            let prop = new MultiProperty();
            prop.Slot = slot.slot;
            prop.Param = property["par"];
            prop.PropertyId = property["prop"];
            prop.Max = property["Max"];
            prop.Min = property["Min"];
            prop.FormattedString = property["parsed"];
            props.push(prop);
        }
    }
    return props;
}
