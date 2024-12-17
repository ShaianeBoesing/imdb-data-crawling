"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.UnifiedService = void 0;
const common_1 = require("@nestjs/common");
const fs_1 = require("fs");
const path = require("path");
let UnifiedService = class UnifiedService {
    getUnifiedData() {
        const filePath = path.join(__dirname, '../../src/data/unified.json');
        const jsonData = (0, fs_1.readFileSync)(filePath, 'utf-8');
        return JSON.parse(jsonData);
    }
};
exports.UnifiedService = UnifiedService;
exports.UnifiedService = UnifiedService = __decorate([
    (0, common_1.Injectable)()
], UnifiedService);
//# sourceMappingURL=unified.service.js.map