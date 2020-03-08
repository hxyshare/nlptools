# -*- coding: utf-8 -*-
import os 

class TrieNode:
        # Initialize your data structure here.
        def __init__(self,depth):
            self.isword=False
            self.frequence=None
            self.depth=depth
            self.children={}
    
class Trie:
    
        def __init__(self):
            self.root = TrieNode(0)

        def insert(self, word):
            node=self.root
            for i in word:
                if i not in node.children:
                    node.children[i]=TrieNode(node.depth + 1)
                node=node.children[i]
            node.isword=True

        def search(self, word):
            '''
            @description:  在字典树中搜素
            @param {type} 
            @return: node.isword(是不是一个完整路径词),word_path(命中的pattern之外的),pattern(pattern)
            '''
            #print(word)
            word_path = ""
            pattern = ""
            node=self.root
            for i in range(len(word)):
                if word[i] not in node.children :
                    #当前字符在当前节点的子节点里面
                    if  "*" in node.children and (word[i] in node.children["*"].children) and i + 1 < len(word):
                    
                        if word[i + 1] not in node.children["*"].children[word[i]].children:
                            word_path += word[i]
                            continue
                        
                        node=node.children["*"]
                    elif "*" in node.children:
                        pattern += "*"
                        word_path += word[i]
                        continue
                    else: 
                        return False,"",""

                pattern += word[i]
                word_path += "*"
                node=node.children[word[i]]

            if node.depth == 0:
                return False,"",""    

            return node.isword,word_path,pattern
 
        def startsWith(self, prefix):
            node=self.root
            for i in prefix:
                if i not in node.children:
                    return False
                node=node.children[i]
            return True
        
        def delete(self, key, sep = ' '):  
                elements = key if isinstance(key, list) else key.split(sep)  
                return self.__delete(elements)  
        
        def __delete(self, elements, node = None, i = 0):  
            node = node if node else self.root  
            e = elements[i]  
            if e in node.children:  
                child_node = node.children[e]  
                if len(elements) == (i+1):  
                    if child_node.frequence is None: return False # not in dict  
                    if len(child_node.children) == 0:  
                        node.children.pop(e)  
                    else:  
                        child_node.frequence = None  
                    return True  
                elif self.__delete(elements, child_node, i+1):  
                    if len(child_node.children) == 0:  
                        return node.children.pop(e)  
                    return True  
            return False  
        
        def shortest_prefix(self, key, default = None, sep = ' '):  
            elements = key if isinstance(key, list) else key.split(sep)  
            results = []  
            node = self.root
            frequence = node.frequence
            for e in elements:  
                if e in node.children:  
                    results.append(e)  
                    node = node.children[e]  
                    frequence = node.frequence  
                    if frequence is not None:  
                        return sep.join(results)  
                else:  
                    break  
            if frequence is None:  
                if default is not None:  
                    return default  
                else:  
                    raise Exception("no item matches any prefix of the given key!")  
            return sep.join(results)  
        
        def longest_prefix(self, key, default = None, sep = ' '):  
            elements = key if isinstance(key, list) else key.split(sep)  
            results = []  
            node = self.root  
            frequence = node.frequence  
            for e in elements:  
                if e not in node.children:  
                        if frequence is not None:  
                            return sep.join(results)  
                        elif default is not None:  
                            return default  
                        else:  
                            raise Exception("no item matches any prefix of the given key!")  
                results.append(e)  
                node = node.children[e]  
                frequence = node.frequence  
            if frequence is None:  
                if default is not None:  
                        return default  
                else:  
                        raise Exception("no item matches any prefix of the given key!")  
            return sep.join(results)  
        
        def longest_prefix_value(self, key, default = None, sep = ' '):  
            elements = key if isinstance(key, list) else key.split(sep)  
            node = self.root  
            frequence = node.frequence  
            for e in elements:  
                if e not in node.children:  
                        if frequence is not None:  
                            return frequence  
                        elif default is not None:  
                            return default  
                        else:  
                            raise Exception("no item matches any prefix of the given key!")  
                node = node.children[e]  
                frequence = node.frequence  
            if frequence is not None:  
                return frequence  
            if default is not None:  
                return default  
            raise Exception("no item matches any prefix of the given key!")  
        
        def longest_prefix_item(self, key, default = None, sep = ' '):  
            elements = key if isinstance(key, list) else key.split(sep)  
            node = self.root  
            frequence = node.frequence  
            results = []  
            for e in elements:  
                if e not in node.children:  
                        if frequence is not None:  
                            return (sep.join(results), frequence)  
                        elif default is not None:  
                            return default  
                        else:  
                            raise Exception("no item matches any prefix of the given key!")  
                results.append(e)  
                node = node.children[e]  
                frequence = node.frequence  
            if frequence is not None:  
                return (sep.join(results), frequence)  
            if default is not None:  
                return (sep.join(results), default)  
            raise Exception("no item matches any prefix of the given key!")  
        
        def __collect_items(self, node, path, results, sep):  
            if node.frequence is not None:  
                results.append((sep.join(path), node.frequence))  
            for k, v in node.children.iteritems():  
                path.append(k)  
                self.__collect_items(v, path, results, sep)  
                path.pop()  
            return results    
        
        def items(self, prefix, sep = ' '):  
                elements = prefix if isinstance(prefix, list) else prefix.split(sep)  
                node = self.root  
                for e in elements:  
                    if e not in node.children:  
                        return []  
                    node = node.children[e]  
                results = []  
                path = [prefix]  
                self.__collect_items(node, path, results, sep)  
                return results  
            
        def keys(self, prefix, sep = ' '):  
                items = self.items(prefix, sep)  
                return [key for key,frequence in items]

def test_xiaoaiquery():
    
    trie = Trie()
    base_path = "/home/zixiang/DataSets/berttestdata/xiaoaiquerylog"
    raw_train_paths = os.path.join(base_path,"xiaoai_v2.txt")

    count = 0
    for line in open("/home/zixiang/Projects/text_correction/codebase/data/pattern.txt"):
        tmp_pattern = [i for i in line.strip().split("\t")[0]]
        
        if len(tmp_pattern) < 3:
            print(tmp_pattern)
            continue

        trie.insert(tmp_pattern)

        count += 1
        if count == 5000:
            break

    count = 0
    for line in open(raw_train_paths):
        isword,word_path,pattern= trie.search([i for i in line.strip()])
        pattern_list = [i for i in pattern.split("*") if i ]
        if len(pattern_list) == 1 and len(pattern_list[0]) == 1:
            #print(pattern)
            continue
        if not isword and len(word_path) ==  0:
            continue
        else:
            count += 1

        if count % 10000 == 0:
            print(count)
            print("word:",word_path,"<---->","pattern:",pattern,isword)
        # if "你给我" in pattern:
        #     print("word:",word_path,"<---->","pattern:",pattern,isword)

def test():
    trie = Trie()
    trie.insert("怎 么 样 预 防 *".strip().split())
    trie.insert("怎 么 *".strip().split())
    trie.insert("怎 么 样 哈 哈 *".strip().split())
    trie.insert("* 怎 么 样 预 防".strip().split())
    trie.insert("你 给 我 唱 一 首 歌 *".strip().split())
    trie.insert("你 给 我 *".strip().split())

    trie.insert("小 孩 * 怎 么 办".strip().split())
    trie.insert("小 孩 *".strip().split())
    trie.insert("小 孩 * 怎 么 怎 么 办".strip().split())
    # trie.insert("什 么 是 *".strip().split())
    # trie.insert("什 么 是 *".strip().split())
    # trie.insert("播 放 * 的 新 闻".strip().split())
    # trie.insert("播 放 * 的 新 闻 * 怎 么 样".strip().split()
    # trie.insert("帮 我 看 一 下 *".strip().split())
    # trie.insert("帮 我 *".strip().split())
    
    print(trie.search("怎 么 样 预 防 是 地 是 方 武 汉 肺 是 啊".strip().split()))
    print(trie.search("怎 么 样 预 防 是 地 是 方 武 汉 肺 是".strip().split()))
    print(trie.search("怎 么 样 预 防 是 地 是 方 武 汉 肺 是".strip().split()))
    print(trie.search("怎 么 样 预 防 是 地 是 方 武 汉 肺 是".strip().split()))
    print(trie.search("你 给 我 唱 一 首 歌 随 便".strip().split()))
    print(trie.search("你 给 我 唱 一 首 歌 随 便".strip().split()))

    print(trie.search("小 孩 同 学".strip().split()))
    print(trie.search("小 孩 哭 了 怎 么 办".strip().split()))

    # print(trie.search("播 放 * 的 新 闻".strip().split()))
    # print(trie.search("播 放 武 汉 是 地 方 的 新 闻 啊 的 怎 么 样".strip().split()))
    # print(trie.search("是 地 方 肺 炎 怎 么 样 预 防".strip().split()))
    # print(trie.search("预 防 是 地 方 肺 炎".strip().split()))
    # print(trie.search("撒 地 方 防 是 地 方 肺 炎".strip().split()))
    # print(trie.search("怎 么 样 预 防 是 地 是 方 武 汉 肺 是".strip().split()))
    # print(trie.search("武 汉 肺 炎 是 什 么 呀".strip().split()))
    # print(trie.search("什 么 是 是 地 方 汉 肺 炎".strip().split()))
    # print(trie.search("什 么 哈 哈 地 方 汉 肺 炎".strip().split()))
    # print(trie.search("帮 我 看 一 下 团 贷 网 的 最 新 消 息".strip().split()))

if __name__ == "__main__":
    
    #test()
    test_xiaoaiquery()
